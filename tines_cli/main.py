from typer             import Typer
from os                import getenv
from dotenv            import load_dotenv
from tines_cli         import __version__
from .commands.tenant  import tenant_typer
from .commands.envvars import envvars_typer
from tapi.utils.http   import disable_ssl_verification


typer = Typer(add_completion = False)
typer.add_typer(tenant_typer)
typer.add_typer(envvars_typer)

@typer.command(help = "Tool version")
def version():
    print(__version__)

@typer.callback()
def callback(invoke_without_command = True):
    load_dotenv()

    DISABLE_SSL = getenv("DISABLE_SSL")

    if DISABLE_SSL == "1":
        disable_ssl_verification()

def main():
    typer()