from typer            import Typer
from .commands.tenant import tenant_typer

def main():
    typer = Typer(add_completion = False)
    typer.add_typer(tenant_typer)

    typer()