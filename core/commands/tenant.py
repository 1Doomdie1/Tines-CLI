from requests          import get
from rich.table        import Table
from rich              import print
from typing_extensions import Annotated
from json              import dump, loads, load
from dotenv            import load_dotenv, set_key
from os.path           import exists, abspath, join
from typer             import Typer, Argument, Option
from os                import remove, environ, scandir

app = Typer()

@app.command(help="Add tenant locally")
def add(
    domain:    Annotated[str,  Argument(...,          help="Tenant domain ID"                   )],
    api_key:   Annotated[str,  Argument(...,          help="User API key"                       )],
    checkout_: Annotated[bool, Option  ("--checkout", help="Use tenant"                         )] = False,
    overwrite: Annotated[bool, Option  (...,          help="Overwrite local tenant confing file")] = False
):
    file_name = domain.lower().replace("-", "_")
    file_path = join(abspath(f"tenants/{file_name}.json"))
    URL       = f"https://{domain}.tines.com/api/v1/info"
    HEADERS   = {"Authorization": f"Bearer {api_key}"}

    if not exists(file_path) or overwrite:
        req = get(URL, headers=HEADERS)
        if req.status_code == 200:
            with open(file_path, "w") as file:
                dump({
                    "domain": domain,
                    "api_key": api_key
                }, file, indent=4)
            print(f"[[bold green]+[/bold green]] Succesfully added tenant: {domain}")
            if checkout_: checkout(domain)
        else:
            print(f"[[bold red]-[/bold red]][bold red] Invalid credentials[/bold red]")
    else:
        print(f"[[bold red]-[/bold red]] Tenant [bold red]{domain}[/bold red] is already present. If you wish to overwrite the config file use the [bold green]'--overwrite'[/bold green] flag")

@app.command(help="Delete local tenant")
def delete(
    domain: Annotated[str, Argument(..., help="Tenant domain id")]
):
    try:
        file_name = domain.lower().replace("-", "_")
        file_path = join(abspath(f"tenants/{file_name}.json"))
        remove(file_path)
    except FileNotFoundError:
        print(f"[[bold red]-[/bold red]] No tenant named: [bold red]{domain}[/bold red]")


@app.command(help="Switch to other tenants")
def checkout(
    domain: Annotated[str, Argument(..., help="Tenant ID")]
):
    file_name = domain.lower().replace("-", "_")
    file_path = join(abspath(f"tenants/{file_name}.json"))
    if exists(file_path):
        load_dotenv()
        set_key(abspath(".env"), "TENANT_DOMAIN", domain)
        print(f"[[bold green]+[/bold green]] Switched to '{domain}' tenant")
    else:
        print(f"[[bold red]+[/bold red]] Domain '[bold red]{domain}[/bold red]' does is not present locally. If you wish to add it try 'py tines.py tenant add' command")


@app.command(help="Show tenant details")
def info():
    load_dotenv()

    with open(abspath(f"tenants/{environ["TENANT_DOMAIN"].replace('-', '_')}.json")) as file:
        data = load(file)
        DOMAIN  = data["domain"]
        API_KEY = data["api_key"]

    URL     = f"https://{DOMAIN}.tines.com/api/v1/info"
    HEADERS = {"Authorization": f"Bearer {API_KEY}"}

    req = loads(get(URL, headers=HEADERS).content)["stack"]
    
    TABLE = Table()
    TABLE.add_column("Name",       justify="center")
    TABLE.add_column("Type",       justify="center")
    TABLE.add_column("Region",     justify="center")
    TABLE.add_column("Egress IPs", justify="center")

    TABLE.add_row(req["name"], req["type"], req["region"], "\n".join(req["egress_ips"]))
    
    print(TABLE)


@app.command(name="list", help="List all local available tenants")
def _list():
    TENANTS_PATH = abspath("tenants")
    
    TABLE = Table()
    TABLE.add_column("Domain Name", justify="center")

    for entry in scandir(TENANTS_PATH):
        if entry.is_file():
            TABLE.add_row(entry.name.replace(".json", ""))
    
    print(TABLE)