from os.path           import join
from os                import getcwd
from typing_extensions import Annotated
from typer             import Typer, Argument, Option
from dotenv            import set_key, dotenv_values, unset_key

envvars_typer = Typer(name = "envars", help = "Manage utility environment variables")

@envvars_typer.command(name="set", help="Set environment variables")
def set_(
        key:   Annotated[str, Argument(..., help="Env var key")],
        value: Annotated[str, Argument(..., help="Env var value")]
):
    set_key(".env", key, value)

@envvars_typer.command(name = "list", help = "List environment variables")
def list_():
    for key, value in dotenv_values(".env").items():
        print(f"{key}: {value}")

@envvars_typer.command(name = "export", help = "Export environment variables")
def export(
        export_path: Annotated[str,  Option("--export-path", "--ep", help = "Export path. Current working directory")] = join(getcwd(), "env_export.txt")
):
    vars_to_export = ""
    for key, value in dotenv_values(".env").items():
        vars_to_export += f"{key}='{value}'\n"

    if vars_to_export:
        try:
            with open(export_path, "w") as file:
                file.write(vars_to_export.strip())

            print(f"[+] Successfully exported to: {export_path}")
        except OSError:
            print("[-] Export filename is missing.")
    else:
        print("[-] No vars to export")

@envvars_typer.command(name = "set", help = "Set environment variable")
def set_(
        var: Annotated[str, Argument(..., help = "Var name")],
        val: Annotated[str, Argument(..., help = "Var value")]
):
    var = var.strip().upper()
    set_key(".env", var, val)
    print(f"[+] Variable '{var}' has been set")

@envvars_typer.command(help = "Unset environment variable")
def unset(
        var: Annotated[str, Argument(..., help = "Var name")]
):
    var = var.strip().upper()
    success, _ = unset_key(".env", var)
    if success:
        print(f"[+] Variable '{var}' has been unset")

@envvars_typer.command(name = "import", help = "Import environment variable")
def import_(
        path: Annotated[str, Argument(..., help = "File path")]
):
    with open(path, "r") as file:
        vars_to_import = [env_pairs.split("=") for env_pairs  in file.read().split("\n")]

    for env_pair in vars_to_import:
        set_key(".env", env_pair[0], env_pair[1], quote_mode="never")