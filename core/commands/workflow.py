from core.commands.types            import *
from typing_extensions              import Annotated
from core.managers.workflow_manager import WorkflowManager
from typer                          import Typer, Argument, Option

app = Typer()

@app.command(help="Create workflow")
def create(
    name:            Annotated[str,                  Argument(..., help="The story name"                                                                )],
    team_id:         Annotated[int,                  Option  (..., help="ID of team to which the story should be added"                                 )],
    description:     Annotated[str,                  Option  (..., help="A user-defined description of the story"                                       )] = "Created with tines_cli",
    keep_events_for: Annotated[keep_events_for_type, Option  (..., help="Event retention period"                                                        )] = keep_events_for_type._1d,
    folder_id:       Annotated[int | None,           Option  (..., help="ID of folder to which the story should be added"                               )] = None,
    tags:            Annotated[str,                  Option  (..., help="An array of Strings separated by ',' used to create tags to classify the story")] = "",
    disabled:        Annotated[bool,                 Option  (..., help="Boolean flag indicating whether the story is disabled"                         )] = False,
    priority:        Annotated[bool,                 Option  (..., help="Boolean flag indicating if this is a high priority story"                      )] = False
):
    WorkflowManager.create_workflow(team_id, name, description, keep_events_for, folder_id, tags, disabled, priority)

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
