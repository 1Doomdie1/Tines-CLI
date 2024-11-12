from typer import Typer
from core.commands.tenant   import app as tenant_app
from core.commands.workflow import app as workflow_app

app = Typer(add_completion=False)
app.add_typer(workflow_app, name="workflow", help="Manage workflows")
app.add_typer(tenant_app,   name="tenant",   help="Mange tenants")

if __name__ == "__main__":
    app()