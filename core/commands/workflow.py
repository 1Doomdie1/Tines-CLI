from typing_extensions import Annotated
from typer             import Typer, Argument, Option

app = Typer()

@app.command(help="Create workflow")
def create(
    name:        Annotated[str, Argument(..., help="Workflow name"       )],
    description: Annotated[str, Option  (..., help="Workflow description")] = "Created with tines_cli",
    location:    Annotated[int, Option  (..., help="Folder id"           )] = None
):

    ...
@app.command(help="Get workflow logs")
def logs(
    id:      Annotated[int, Argument(..., help="Workflow ID")],
    filters: Annotated[str, Option  (..., help="Filter logs")] = None
):
    ...

@app.command(help="Get workflow details")
def info(
    id: Annotated[int, Argument(..., help="Workflow ID")]
):
    ...

@app.command(help="Archive workflow")
def archive(
    id: Annotated[int, Argument(..., help="Workflow ID")]
):
    ...

@app.command(help="Delete workflow")
def delete(
    id: Annotated[int, Argument(..., help="Workflow ID")]
):
    ...

@app.command(name="list", help="List all workflows in the tenant")
def _list(
    id: Annotated[int, Argument(..., help="Workflow ID")]
):
    ...
