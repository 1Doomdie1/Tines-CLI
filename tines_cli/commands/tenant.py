from click             import Choice
from tapi              import TenantAPI
from typing_extensions import Annotated
from prettytable       import PrettyTable
from typer             import Typer, Context
from typer             import Argument, Option
from json              import load, dump, dumps


tenant_typer = Typer(name = "tenant", help = "Manage tenant(s)")

@tenant_typer.command(help = "Add tenant locally")
def add(
        ctx:      Context,
        domain:   Annotated[str,  Argument(..., help = "Tenant domain"  )],
        api_key:  Annotated[str,  Argument(..., help = "User API key"   )],
        checkout: Annotated[bool, Option  (..., help = "Checkout domain")] = False
):
    tenant = TenantAPI(domain, api_key)
    req = tenant.info()
    status_code = req.get("status_code")

    if status_code == 200:
        new_tenant_creds = {"domain": domain, "api_key": api_key, "checkout": checkout}

        with open(ctx.obj["TENANTS_FILE"], "r") as file:
            tenants = load(file)

            for index, tenant in enumerate(tenants):
                if tenant.get("domain") == domain:
                    print("[!] Domain already exists")
                    return

            tenants.append(new_tenant_creds)

        with open(ctx.obj["TENANTS_FILE"], "w") as file:
            dump(tenants, file, indent = 4)

        if checkout:
            checkout_(ctx, domain)

        print("[+] Successfully added tenant")
    else:
        print("[-] Invalid domain and/or api key.")
        print("[!] Sometimes SSL verification can mess this process up. Make sure you disable it by using this command and try again:")
        print("    -> tines envars set disable_ssl 1")

@tenant_typer.command(name = "checkout", help = "Change to a particular tenant")
def checkout_(
        ctx:    Context,
        domain: Annotated[str, Argument(..., help = "Tenant domain")]
):
    current_checked_out_tenant = ctx.obj.get("DOMAIN")

    if current_checked_out_tenant == domain:
        print("[!] Already checked out on this tenant!")
        exit()

    with open(ctx.obj.get("TENANTS_FILE"), "r") as file:
        tenants = load(file)

    domain_exists = any(tenant.get("domain") == domain for tenant in tenants)

    if not domain_exists:
        print(f"[-] No such tenant '{domain}' found.")
        exit()

    for index, tenant in enumerate(tenants):
        if tenant.get("domain") == current_checked_out_tenant:
            tenants[index]["checkout"] = False

        if tenant.get("domain") == domain:
            tenants[index]["checkout"] = True

    with open(ctx.obj.get("TENANTS_FILE"), "w") as file:
        dump(tenants, file, indent = 4)

    print(f"[+] Successfully checked out tenant '{domain}'")

@tenant_typer.command(help = "Pull tenant information")
def info(
        ctx:       Context,
        output_as: Annotated[str,  Option(..., click_type = Choice(["json", "table"]))] = "table"
):
    DOMAIN  = ctx.obj.get("DOMAIN",  None)
    API_KEY = ctx.obj.get("API_KEY", None)

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
            table = PrettyTable()
            table.field_names = ["Domain", "SV Name", "Type", "Region", "Egress IPs"]

            table.add_row(
                [
                    DOMAIN,
                    stack.get("name"),
                    stack.get("type"),
                    stack.get("region"),
                    ", ".join(stack.get("egress_ips"))
                ]
            )
            print(table)
    else:
        print(f"[-] Error encountered: ")
        print(f"    -> Status code: {status_code}")
        print(f"    -> Message: {req.get('body')}")

@tenant_typer.command(name = "list", help = "List all the tenants saved locally")
def _list(
        ctx:       Context,
        output_as: Annotated[str, Option(..., click_type=Choice(["json", "table"]))] = "table"
):

    with open(ctx.obj.get("TENANTS_FILE"), "r") as file:
        tenants_data = load(file)

    if not tenants_data:
        print("[!] No tenants!")
        return

    if output_as == "json":
        tenants = [{"domain": tenant.get("domain")} for tenant in tenants_data]
        print(dumps(tenants, indent = 4))
    else:
        table = PrettyTable()
        table.field_names = ["Nr", "Domain", "In use"]
        table.add_rows([[index, tenant.get("domain"), "✓" if tenant.get("checkout") else "✗"]for index, tenant in enumerate(tenants_data, 1)])
        print(table)

@tenant_typer.command(help = "Delete local tenant")
def delete(
        ctx:    Context,
        domain: Annotated[str, Argument(..., help = "Tenant domain")]
):
    with open(ctx.obj.get("TENANTS_FILE"), "r") as file:
        tenants = load(file)

    for index, tenant in enumerate(tenants):
        if tenant.get("domain") == domain:
            tenants.pop(index)
            with open(ctx.obj.get("TENANTS_FILE"), "w") as file:
                dump(tenants, file, indent = 4)
            print(f"[+] Successfully removed tenant")
            return

    print(f"[!] No such tenant '{domain}' found")
    return
