from typer             import Typer
from .commands.tenant  import tenant_typer
from .commands.envvars import envvars_typer

def main():
    typer = Typer(add_completion = False)
    typer.add_typer(tenant_typer)
    typer.add_typer(envvars_typer)

    typer()