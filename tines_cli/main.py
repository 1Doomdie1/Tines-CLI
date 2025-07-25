from os                 import getenv
from os                 import makedirs
from json               import dump, load
from dotenv             import load_dotenv
from tines_cli          import __version__
from .commands.utils    import utils_typer
from .commands.tenant   import tenant_typer
from .commands.workflow import workflow_typer
from typer              import Typer, Context
from tapi.utils.http    import disable_ssl_verification
from os.path            import join, dirname, abspath, exists


typer = Typer(add_completion = False)
typer.add_typer(utils_typer)
typer.add_typer(tenant_typer)
typer.add_typer(workflow_typer)


@typer.command(help = "Tool version")
def version():
    print(__version__)


@typer.callback()
def callback(ctx: Context):
    # Load env vars and create an empty context object
    load_dotenv()
    ctx.obj = {}

    # Load context with data
    ctx.obj["DISABLE_SSL"]    = getenv("DISABLE_SSL")
    ctx.obj["TENANTS_FILE"]   = join(dirname(abspath(__file__)), "tenants.json")
    ctx.obj["EXPORTS_FOLDER"] = join(dirname(abspath(__file__)), "exports")

    # Disable SSL if needed
    if getenv("DISABLE_SSL") == "1":
        disable_ssl_verification()

    # Check if TENANTS_FILE exists; If it doesn't create an empty file
    if not exists(ctx.obj["TENANTS_FILE"]):
        with open(ctx.obj["TENANTS_FILE"], "w") as file:
            dump([], file, indent=4)

    # Check if EXPORTS_FOLDER exists; If it doesn't create an empty folder
    if not exists(ctx.obj["EXPORTS_FOLDER"]):
        makedirs(ctx.obj["EXPORTS_FOLDER"])

    # Set DOMAIN and API_KEY to context
    with open(ctx.obj["TENANTS_FILE"], "r") as file:
        tenants = load(file)

    tenant = next((tenant for tenant in tenants if tenant.get("checkout") == True), None)

    if tenant:
        ctx.obj["DOMAIN"]  = tenant["domain"]
        ctx.obj["API_KEY"] = tenant["api_key"]


def main():
    typer()