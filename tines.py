from rich.console           import Console 
from dotenv                 import set_key
from os                     import makedirs
from typer                  import Typer, Context
from os.path                import abspath, exists
from core.commands.team     import app as team_app
from core.commands.tenant   import app as tenant_app
from core.commands.workflow import app as workflow_app


app = Typer(add_completion=False)
app.add_typer(workflow_app, name="workflow", help="Manage workflows")
app.add_typer(tenant_app,   name="tenant",   help="Manage tenants")
app.add_typer(team_app,     name="team",     help="Manage teams")

@app.callback()
def check_creds(
    ctx: Context = Context
) -> None:
    # Set Global Context
    ctx.obj = {"console": Console(log_path=False)}

    # Folder Paths
    exports_path = abspath("exports")
    tenants_path = abspath("tenants")

    # File Paths
    dotenv_path = abspath(".env")
    
    # Create folders if they do not exist
    makedirs(exports_path, exist_ok=True)
    makedirs(tenants_path, exist_ok=True)

    # Create .env file if it doesn't exist
    if not exists(dotenv_path):
        with open(dotenv_path, "w"):
            set_key(dotenv_path, "USE_TENANT", "None")

if __name__ == "__main__":
    app()