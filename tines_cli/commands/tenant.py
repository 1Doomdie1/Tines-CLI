from hashlib           import md5
from typer             import Typer
from click             import Choice
from os                import getenv
from tapi              import TenantAPI
from typing_extensions import Annotated
from prettytable       import PrettyTable
from typer             import Argument, Option
from json              import load, dump, dumps
from dotenv            import load_dotenv, set_key
from tapi.utils.http   import disable_ssl_verification
from os.path           import dirname, join, abspath, exists


tenant_typer = Typer(name = "tenant", help = "Manage tenant(s)")
tenants_json_file = join(dirname(dirname(abspath(__file__))), "tenants.json")

@tenant_typer.command(help = "Add tenant locally")
def add(
        domain:      Annotated[str,  Argument(..., help = "Tenant domain"                      )],
        api_key:     Annotated[str,  Argument(..., help = "User API key"                       )],
        checkout:    Annotated[bool, Option  (..., help = "Checkout this tenant after creation")] = False,
        disable_ssl: Annotated[bool, Option  (..., help = "Disable SSL verification"           )] = False
):
    if disable_ssl:
        disable_ssl_verification()

    tenant = TenantAPI(domain, api_key)
    req = tenant.info()
    status_code = req.get("status_code")

    if status_code == 200:
        md5hash = md5()
        md5hash.update(f"{domain}:{api_key}".encode("utf-8"))
        new_tenant_creds = {"domain": domain, "api_key": api_key, "md5": md5hash.hexdigest()}

        if exists(tenants_json_file):
            with open(tenants_json_file, 'r', encoding='utf-8') as file_data:
                data = load(file_data)
            tenants_md5_hashes = [tenant["md5"] for tenant in data]

            if new_tenant_creds["md5"] in tenants_md5_hashes:
                print("[!] Tenant is already added.")
                return
            data.append(new_tenant_creds)
        else:
            data = [new_tenant_creds]

        with open(tenants_json_file, "w") as file:
            dump(data, file, indent=4)

        if checkout:
            load_dotenv()
            set_key(".env", "DOMAIN", domain)
            set_key(".env", "API_KEY", api_key)
            print(f"[+] Now using \"{domain}\" tenant")

        print(f"[+] Tenant {domain} has been added successfully")
    elif status_code == 401:
        print("[-] Invalid domain or API key")
    else:
        print(req.get("body"))

@tenant_typer.command(help = "Pull tenant information")
def info(
        output_as:   Annotated[str,  Option(..., click_type = Choice(["json", "table"]))] = "table",
        disable_ssl: Annotated[bool, Option(..., help = "Disable SSL verification")] = False
):
    if disable_ssl:
        disable_ssl_verification()

    load_dotenv()
    DOMAIN = getenv("DOMAIN")
    API_KEY = getenv("API_KEY")

    if not DOMAIN or not API_KEY:
        print("[-] Please checkout a tenant first.")
        print("[-] Use: tines tenant checkout --help")
        return

    tenant = TenantAPI(DOMAIN, API_KEY)
    req = tenant.info()
    status_code = req.get("status_code")

    if status_code == 200:
        if output_as == "json":
            print(dumps(req.get("body"), indent = 4))
        else:
            stack = req.get("body").get("stack")
            # print(stack.get("name"))
            table = PrettyTable()
            table.field_names = ["Name", "Type", "Region", "Egress IPs"]

            table.add_row(
                [
                    stack.get("name"),
                    stack.get("type"),
                    stack.get("region"),
                    ", ".join(stack.get("egress_ips"))
                ]
            )
            print(table)
    else:
        print("[-] Error encountered: ")
        print(f"[!] Status code: {status_code}")
        print(f"[!] Message: {req.get('body')}")

@tenant_typer.command(name = "list", help = "List all the tenants saved locally")
def _list(
        output_as: Annotated[str, Option(..., click_type=Choice(["json", "table"]))] = "table"
):
    if not exists(tenants_json_file):
        print("[-] No tenants have been added. Please use 'tines tenant add <DOMAIN> <API_KEY>' command")
        return

    with open(tenants_json_file, "r") as file:
        tenants_data = load(file)

    if not tenants_data:
        print("[!] No tenants!")
        return

    if output_as == "json":
        tenants = [{"domain": tenant.get("domain"), "md5": tenant.get("md5")} for tenant in tenants_data]
        print(dumps(tenants, indent = 4))
    else:
        table = PrettyTable()
        table.field_names = ["Nr", "Domain", "MD5"]
        table.add_rows([[index, tenant.get("domain"), tenant.get("md5")]for index, tenant in enumerate(tenants_data, 1)])
        print(table)

@tenant_typer.command(help = "Delete local tenant")
def delete(
        tenant_md5: Annotated[str, Argument(..., help = "Domain's md5 to delete")]
):
    if not exists(tenants_json_file):
        print("[-] No tenants have been added. Please use 'tines tenant add <DOMAIN> <API_KEY>' command")
        return

    load_dotenv()

    with open(tenants_json_file, "r") as file:
        tenants_data = load(file)

    for index, tenant in enumerate(tenants_data):
        if tenant.get("md5") == tenant_md5:
            tenants_data.pop(index)

            with open(tenants_json_file, "w") as file:
                dump(tenants_data, file, indent = 4)

            if getenv("DOMAIN") == tenant.get("domain") and getenv("API_KEY") == tenant.get("api_key"):
                set_key(".env", "DOMAIN", "")
                set_key(".env", "API_KEY", "")
                print(f"[+] Checked out from '{tenant.get("name")}' tenant")

            print(f"[+] Successfully removed tenant '{tenant.get("name")}'")

            return

    print(f"[!] No tenant found with hash: {tenant_md5}")

@tenant_typer.command(help = "Switch to other tenants")
def checkout(
        domain  :    Annotated[str,  Option(..., help = "Domain name")]              = None,
        md5_hash:    Annotated[str,  Option(..., help = "Domain md5")]               = None,
        disable_ssl: Annotated[bool, Option(..., help = "Disable ssl verification")] = None,
):

    if not domain and not md5_hash:
        print("[-] One of domain or md5_hash must be specified")
        return

    if domain and md5_hash:
        print("[-] Only domain or md5_hash must be specified but not both")
        return

    if not exists(tenants_json_file):
        print("[-] No tenants have been added. Please use 'tines tenant add <DOMAIN> <API_KEY>' command")
        return

    if disable_ssl:
        disable_ssl_verification()

    load_dotenv()

    with open(tenants_json_file, "r") as file:
        tenant_data = load(file)

    for tenant in tenant_data:
        if tenant.get("domain") == domain or tenant.get("md5") == md5_hash:

            if getenv("DOMAIN") == tenant.get("domain"):
                print("[!] Already using this tenant")
                return

            tnt = TenantAPI(tenant.get("domain"), tenant.get("api_key"))
            req = tnt.info()
            status_code = req.get("status_code")

            if status_code == 200:
                set_key(".env", "DOMAIN", tenant.get("domain"))
                set_key(".env", "API_KEY", tenant.get("api_key"))

                print(f"[+] Now using the '{tenant.get("domain")}' tenant")
                return

            print("[!] Unable to checkout. Possible reasons:")
            print("    -> API key was revoked")
            print("    -> Tenant was deleted")
            print("    -> Network issues (This can be due to SSL. Try using the '--disable-ssl' flag)")
            return

    print("[-] Unable to find the specified tenant.")
    print("[-] If the tenant is already added please check for spelling mistakes.")
    print("[-] Recommended commands:")
    print("\t-> tines tenant add <DOMAIN> <API_KEY>")
    print("\t-> tines tenant list")
