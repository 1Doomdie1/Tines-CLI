from rich.table                   import Table
from rich                         import print
from typing_extensions            import Annotated
from core.managers.tenant_manager import TenantManager
from typer                        import Typer, Argument, Option

app = Typer()

@app.command(help="Add tenant locally")
def add(
    domain:    Annotated[str,  Argument(...,          help="Tenant domain ID"                   )],
    api_key:   Annotated[str,  Argument(...,          help="User API key"                       )],
    checkout_: Annotated[bool, Option  ("--checkout", help="Use tenant"                         )] = False,
    overwrite: Annotated[bool, Option  (...,          help="Overwrite local tenant confing file")] = False
):
    TenantManager.add_tenant(domain, api_key, checkout_, overwrite)

@app.command(help="Delete local tenant")
def delete():
    TenantManager.delete_tenant()

@app.command(help="Switch to other tenants")
def checkout(
    domain: Annotated[str, Argument(..., help="Tenant ID")]
):
    TenantManager.checkout_tenant(domain)

@app.command(help="Show all teams in the tenant")
def teams():
    TABLE = Table()
    TEAMS = TenantManager.tenant_teams()

    TABLE.add_column("ID",   justify="center")
    TABLE.add_column("Name", justify="center")

    for team in TEAMS:
        TABLE.add_row(str(team["id"]), team["name"])

    print(TABLE)

@app.command(help="Show tenant details")
def info():

    tenant_data = TenantManager.enpoint_call("GET", "api/v1/info")["data"]["stack"]
    
    TABLE = Table()
    TABLE.add_column("Name",       justify="center")
    TABLE.add_column("Type",       justify="center")
    TABLE.add_column("Region",     justify="center")
    TABLE.add_column("Egress IPs", justify="center")

    TABLE.add_row(tenant_data["name"], tenant_data["type"], tenant_data["region"], "\n".join(tenant_data["egress_ips"]))
    
    print(TABLE)


@app.command(name="list", help="List all local available tenants")
def _list():
    
    TENANTS = TenantManager.list_local_tenants()
    
    TABLE = Table()
    TABLE.add_column("Domain Name", justify="center")

    for tenant in TENANTS:
        TABLE.add_row(tenant.replace(".json", ""))
    
    print(TABLE)