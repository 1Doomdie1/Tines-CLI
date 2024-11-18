from core.utils.types               import *
from json                           import dump
from pathlib                        import Path
from rich.table                     import Table
from rich.console                   import Console
from typing_extensions              import Annotated
from os.path                        import abspath, join
from core.managers.workflow_manager import WorkflowManager
from os                             import makedirs, scandir
from typer                          import Typer, Argument, Option, Context, Exit


EXPORTS_PATH = abspath("exports")
CONSOLE = Console(log_path=False)

app = Typer()

@app.callback()
def manage_team_flags(
    ctx: Context,
    wid: int = Option(None, help="Workflow ID"),
) -> None:
    ctx.obj = {"wid": wid}

    if ctx.invoked_subcommand in {"info", "update", "delete", "export"} and wid is None:
        CONSOLE.log("Error: --wid is required for this command.")
        CONSOLE.log("Usage: tines workflow --wid=<ID> (update | info | delete | export)")
        raise Exit(1)


@app.command(help="Create workflow")
def create(
    name:            Annotated[str,                  Argument(..., help="The story name"                                                                )],
    team_id:         Annotated[int,                  Option  (..., help="ID of team to which the story should be added"                                 )],
    description:     Annotated[str,                  Option  (..., help="A user-defined description of the story"                                       )] = "Created with Tines-CLI",
    keep_events_for: Annotated[keep_events_for_type, Option  (..., help="Event retention period"                                                        )] = keep_events_for_type._1d,
    folder_id:       Annotated[int | None,           Option  (..., help="ID of folder to which the story should be added"                               )] = None,
    tags:            Annotated[str | None,           Option  (..., help="An array of Strings separated by ',' used to create tags to classify the story")] = None,
    disabled:        Annotated[bool,                 Option  (..., help="Boolean flag indicating whether the story is disabled"                         )] = False,
    priority:        Annotated[bool,                 Option  (..., help="Boolean flag indicating if this is a high priority story"                      )] = False
):
    WorkflowManager.create(team_id, name, description, keep_events_for, folder_id, tags, disabled, priority)

@app.command(name="list", help="List all workflows")
def _list(
    team_id:   Annotated[int | None,                         Option(..., help="Return stories belonging to a team"                               )] = None,
    folder_id: Annotated[int | None,                         Option(..., help="Return stories in a speciffic folder"                             )] = None,
    per_page:  Annotated[int,                                Option(..., help="Set the number of results returned per page"                      )] = 100,
    page:      Annotated[int,                                Option(..., help="Specify the page of results to return if there are multiple pages")] = 1,
    tags:      Annotated[str | None,                         Option(..., help="A comma separated list of tag names to filter by"                 )] = None,
    filter:    Annotated[List_Workflows_Filter_Types | None, Option(..., help="Filter by one of"                                                 )] = None,
    order:     Annotated[List_Workflows_Order_Types  | None, Option(..., help="Order the results by one of"                                      )] = None,
    format_as: Annotated[Output_Format_Types,                Option(..., help="Output format"                                                    )] = Output_Format_Types.TABLE
) -> None:
    STORIES = WorkflowManager.list_workflows(team_id, folder_id, per_page, page, tags, filter, order)

    if format_as == Output_Format_Types.TABLE:
        TABLE   = Table()
        COLUMNS = (
            "ID", "Name", 
            "Team ID", "GUID", 
            "Mode", "Folder ID", 
            "Tags", "Disabled", 
            "Priority", "STS"
        )

        for column in COLUMNS:
            TABLE.add_column(column, justify="center")

        for story in STORIES:
            TABLE.add_row(
                f"{story['id']}", story["name"], f'{story["team_id"]}', 
                story["guid"], story["mode"], f'{story["folder_id"]}',
                f'{story["tags"]}', f'{story["disabled"]}', f'{story["priority"]}',
                f'{story["send_to_story_enabled"]}'
            )

        CONSOLE.print(TABLE)
    elif format_as == Output_Format_Types.JSON:
        CONSOLE.log(STORIES)

@app.command(help="Update a story. If change control is enabled on the story the request will be performed on the test story")
def update(
    name:                   Annotated[str | None,                     Option  (..., help="Story name"                                            )] = None,
    description:            Annotated[str | None,                     Option  (..., help="A user-defined description of the story"               )] = None,
    add_tag_names:          Annotated[str | None,                     Option  (..., help="Array of tag names to add to the story"                )] = None,
    remove_tag_names:       Annotated[str | None,                     Option  (..., help="Array of tag names to remove from the story"           )] = None,
    keep_events_for:        Annotated[keep_events_for_type | None,    Option  (..., help="Event retention period"                                )] = None,
    disabled:               Annotated[bool | None,                    Option  (..., help="Indicate whether the story is disabled from running"   )] = None,
    locked:                 Annotated[bool | None,                    Option  (..., help="Indicate whether the story is locked, preventing edits")] = None,
    priority:               Annotated[bool | None,                    Option  (..., help="Indicate whether story runs with high priority"        )] = None,
    sts_access_source:      Annotated[STS_Access_Source_Types | None, Option  (..., help="Indicate where the send to story can be used"          )] = None,
    sts_access:             Annotated[STS_Access_Types | None,        Option  (..., help="Controls who is allowed to send to this story"         )] = None,
    shared_team_slugs:      Annotated[str | None,                     Option  (..., help="List of teams' slugs that can send to this story."     )] = None,
    sts_skill_conf:         Annotated[bool | None,                    Option  (..., help="Skill running confirmation"                            )] = None,
    entry_agent_id:         Annotated[int | None,                     Option  (..., help="The ID of the entry action for this story"             )] = None,
    exit_agent_ids:         Annotated[str | None,                     Option  (..., help="Array of IDs describing exit actions for this story"   )] = None,
    team_id:                Annotated[int | None,                     Option  (..., help="The ID of the team to move the story to"               )] = None,
    folder_id:              Annotated[int | None,                     Option  (..., help="Story ID"                                              )] = None,
    change_control_enabled: Annotated[bool | None,                    Option  (..., help="Indicate if Change Control is enabled"                 )] = None,
    format_as:              Annotated[Output_Format_Types,            Option  (..., help="Output format"                                         )] = Output_Format_Types.TABLE,
    verbose:                Annotated[bool,                           Option  (..., help="Verbose"                                               )] = False,
    ctx:                    Context                                                                                                                 = Context
) -> None:

    UPDATED_VALUES = WorkflowManager.update(
        ctx.obj.get("wid") , name, description, add_tag_names,
        remove_tag_names, keep_events_for, disabled, locked,
        priority, sts_access_source, sts_access, shared_team_slugs,
        sts_skill_conf, entry_agent_id, exit_agent_ids, team_id,
        folder_id, change_control_enabled
    )

    if verbose:
        if format_as == Output_Format_Types.TABLE:
            TABLE = Table()
            TABLE.add_column("Attribute", justify="center")
            TABLE.add_column("Value",     justify="center")

            for attribute, value in UPDATED_VALUES.items():
                TABLE.add_row(attribute.capitalize(), f"{value}")
            CONSOLE.log(TABLE)
        elif format_as == Output_Format_Types.JSON:
            CONSOLE.log(UPDATED_VALUES)

@app.command(help="Get workflow details")
def info(
    mode:      Annotated[Workflow_Modes_Types | None, Option  (..., help="The mode (TEST or LIVE) of the story to retrieve")] = Workflow_Modes_Types.ALL,
    format_as: Annotated[Output_Format_Types,         Option  (..., help="Output format"                                   )] = Output_Format_Types.TABLE,
    ctx:       Context                                                                                                        = Context
) -> None:
    WORKFLOW_DATA = WorkflowManager.get(ctx.obj.get("wid"), mode)

    if format_as == Output_Format_Types.JSON:
        CONSOLE.log(WORKFLOW_DATA)
    elif format_as == Output_Format_Types.TABLE:
        TABLE = Table()
        TABLE.add_column("Attribute", justify="center")
        TABLE.add_column("Value",     justify="center")

        for attribute, value in WORKFLOW_DATA.items():
            TABLE.add_row(attribute, f"{value}")
        CONSOLE.print(TABLE)

@app.command(help="Delete workflow")
def delete(
    ctx: Context = Context
) -> None:
    WorkflowManager.delete(ctx.obj.get("wid"))

@app.command(help="Delete multiple workflows")
def batch_delete(
    ctx: Context = Context
) -> None:
    WorkflowManager.batch_delete(ctx.obj.get("wid"))

@app.command(help="Export workflow")
def export(
    output:         Annotated[Path, Option  (..., help="Output path"                      )] = EXPORTS_PATH,
    randomize_urls: Annotated[bool, Option  (..., help="Randomize webhooks and pages urls")] = False,
    ctx:            Context                                                                  = Context
) -> None:
    makedirs(EXPORTS_PATH, exist_ok=True)

    EXPORT_DATA = WorkflowManager.export(ctx.obj.get("wid"), randomize_urls)

    name = EXPORT_DATA["name"].replace(" ", "_")
    output_path = abspath(join(output, f"{name}.json"))

    with open(output_path, "w") as file:
        dump(EXPORT_DATA, file, indent=4)

    CONSOLE.log("Workflow succesfully exported")
    CONSOLE.log(f"PATH: \'{output_path}\'")

@app.command(name="import", help="Import local workflow to remote tenant")
def _import(
    file:      Annotated[Path,                  Argument(..., help="Path to local workflow"    )],
    new_name:  Annotated[str,                   Option  (..., help="The new name for the story")],
    team_id:   Annotated[int,                   Option  (..., help="Team ID"                   )],
    folder_id: Annotated[int | None,            Option  (..., help="Folder ID"                 )] = None,
    mode:      Annotated[Workflow_Import_Types, Option  (..., help="The new name for the story")] = Workflow_Import_Types.NEW,
) -> None:
    WorkflowManager._import(abspath(file), new_name, team_id, folder_id, mode)

@app.command(help="List all exported workflows")
def exports() -> None:
    makedirs(EXPORTS_PATH, exist_ok=True)

    EXPORTS = [tenant.name for tenant in scandir(EXPORTS_PATH) if tenant.is_file()]

    if EXPORTS:
        TABLE = Table()
        TABLE.add_column("Name", justify="center")

        for entry in EXPORTS:
            TABLE.add_row(entry)
        CONSOLE.print(TABLE)
    else:
        CONSOLE.log("No exports found")