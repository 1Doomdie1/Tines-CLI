from requests          import get
from json              import loads
from os                import remove
from typer             import Option
from typing_extensions import Annotated
from tines_cli         import __version__
from subprocess        import Popen, PIPE
from .envvars          import envvars_typer
from typer             import Typer, Context
from os.path           import join, dirname, abspath, exists


utils_typer = Typer(name = "utils", help = "Utility commands")
utils_typer.add_typer(envvars_typer)

@utils_typer.command(help = "Uninstall tines-cli")
def uninstall(
        verbose: Annotated[bool, Option("--verbose", "--v", help = "Verbosity")] = False
):
    print("[+] Uninstalling...")

    file_paths = [
        join(dirname(dirname(abspath(__file__))), "tenants.json")
    ]

    print("[+] Removing files created by Tines-CLI")
    for path in file_paths:
        if verbose: print(f"{" " * 4}-> {path}", end=" ")
        if exists(path):
            remove(path)
            if verbose: print(" - Done")
        else:
            if verbose: print(" - File not found")

    print("[+] Removing Tines-CLI package (pip)")

    process = Popen(
        ["pip", "uninstall", "tines-cli", "-y"],
        stdout = PIPE,
        stderr = PIPE,
    )

    stdout, stderr = process.communicate()

    if process.returncode == 0:
        if verbose: print(stdout.decode())
    else:
        print(stderr.decode())
        exit()

    print("[+] Done")


@utils_typer.command(help = "Update tool")
def update(
        ctx: Context,
        verbose: Annotated[bool, Option("--verbose", "--v", help = "Verbosity")] = False
):
    print("[+] Checking for updates")
    versions_ = versions(ctx, verbose)

    if f"v{__version__}" == versions_[0]:
        print("[!] App already up to date.")
        exit()
    else:
        print(f"[+] Updating to version {versions_[0]}")

        process = Popen(
            ["pip", "install", "--force-reinstall", f"git+https://github.com/1Doomdie1/Tines-CLI.git@{versions_[0]}"],
            stdout = PIPE,
            stderr = PIPE,
        )

        _, stderr = process.communicate()

        if process.returncode == 0:
            print(f"[+] Tines-CLI is now updated to version {versions_[0]}")
        else:
            print(f"[-] Error encountered:\n{stderr.decode()}")

@utils_typer.command(help = "Get a list of all versions")
def versions(
        ctx:     Context,
        verbose: Annotated[bool, Option("--verbose", "--v", help = "Verbosity")] = False
):
    if verbose: print("[+] Collecting versions...")
    req = get("https://api.github.com/repos/1Doomdie1/Tines-CLI/tags")

    if req.status_code == 200:
        vers = loads(req.content.decode())
        if ctx.command.name == "versions":
            for version in vers:
                print(f"{" ->" if version["name"][1:] == __version__ else " " * 3} {version["name"]}")
        else:
            return [version.get("name") for version in vers]
    else:
        print(f"[!] Error encountered")
        print(f"    -> Status code: {req.status_code}")
        print(f"    -> Message: {req.content.decode()}")