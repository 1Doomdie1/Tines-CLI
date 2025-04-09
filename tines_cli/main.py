from typer             import Typer
from tines_cli         import __version__
from .commands.tenant  import tenant_typer
from .commands.envvars import envvars_typer


typer = Typer(add_completion = False)
typer.add_typer(tenant_typer)
typer.add_typer(envvars_typer)

@typer.command(help = "Tool version")
def version():
    print(__version__)

def main():
    typer()