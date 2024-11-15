from core.commands.types            import *
from rich.table                     import Table
from rich                           import print
from typing_extensions              import Annotated
from core.managers.workflow_manager import WorkflowManager
from typer                          import Typer, Argument, Option

app = Typer()

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
    WorkflowManager.create_workflow(team_id, name, description, keep_events_for, folder_id, tags, disabled, priority)

@app.command(name="list", help="List all workflows")
def _list(
    team_id:   Annotated[int | None,                         Option(..., help="Return stories belonging to a team"                               )] = None,
    folder_id: Annotated[int | None,                         Option(..., help="Return stories in a speciffic folder"                             )] = None,
    per_page:  Annotated[int,                                Option(..., help="Set the number of results returned per page"                      )] = 100,
    page:      Annotated[int,                                Option(..., help="Specify the page of results to return if there are multiple pages")] = 1,
    tags:      Annotated[str | None,                         Option(..., help="A comma separated list of tag names to filter by"                 )] = None,
    filter:    Annotated[List_Workflows_Filter_Types | None, Option(..., help="Filter by one of"                                                 )] = None,
    order:     Annotated[List_Workflows_Order_Types  | None, Option(..., help="Order the results by one of"                                      )] = None,
    format_as: Annotated[Output_Format_Types | None,         Option(..., help="Output format"                                                    )] = Output_Format_Types.TABLE
):
    STORIES = WorkflowManager.list_workflows(team_id, folder_id, per_page, page, tags, filter, order)

    if format_as == Output_Format_Types.TABLE:
        TABLE   = Table()
        COLUMNS = (
            "ID", "Name", "Team ID", 
            "GUID", "Mode", "Folder ID", 
            "Tags", "Disabled", "Priority", 
            "STS"
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

        print(TABLE)
    elif format_as == Output_Format_Types.JSON:
        print(STORIES)


@app.command(help="Update a story. If change control is enabled on the story the request will be performed on the test story")
def update(
    id:                     Annotated[int,                            Argument(..., help="Story ID"                                                                        )],
    name:                   Annotated[str | None,                     Option  (..., help="Story name"                                                                      )] = None,
    description:            Annotated[str | None,                     Option  (..., help="A user-defined description of the story"                                         )] = None,
    add_tag_names:          Annotated[str | None,                     Option  (..., help="Array of tag names to add to the story"                                          )] = None,
    remove_tag_names:       Annotated[str | None,                     Option  (..., help="Array of tag names to remove from the story"                                     )] = None,
    keep_events_for:        Annotated[keep_events_for_type | None,    Option  (..., help="Event retention period"                                                          )] = None,
    disabled:               Annotated[bool | None,                    Option  (..., help="Indicate whether the story is disabled from running"                             )] = None,
    locked:                 Annotated[bool | None,                    Option  (..., help="Indicate whether the story is locked, preventing edits"                          )] = None,
    priority:               Annotated[bool | None,                    Option  (..., help="Indicate whether story runs with high priority"                                  )] = None,
    sts_access_source:      Annotated[STS_Access_Source_Types | None, Option  (..., help="Indicate where the send to story can be used"                                    )] = None,
    sts_access:             Annotated[STS_Access_Types | None,        Option  (..., help="Controls who is allowed to send to this story"                                   )] = None,
    shared_team_slugs:      Annotated[str | None,                     Option  (..., help="List of teams' slugs that can send to this story."                               )] = None,
    sts_skill_conf:         Annotated[bool | None,                    Option  (..., help="Indicate whether workbench should ask for confirmation before running this story")] = None,
    entry_agent_id:         Annotated[int | None,                     Option  (..., help="The ID of the entry action for this story (action must be of type Webhook)"      )] = None,
    exit_agent_ids:         Annotated[str | None,                     Option  (..., help="Array of IDs describing exit actions for this story"                             )] = None,
    team_id:                Annotated[int | None,                     Option  (..., help="The ID of the team to move the story to"                                         )] = None,
    folder_id:              Annotated[int | None,                     Option  (..., help="Story ID"                                                                        )] = None,
    change_control_enabled: Annotated[bool | None,                    Option  (..., help="Indicate if Change Control is enabled"                                           )] = None
):
    kwargs = locals()
    del kwargs['id']

    WorkflowManager.update(id, **kwargs)

# @app.command(help="Get workflow details")
# def info(
#     id: Annotated[int, Argument(..., help="Workflow ID")]
# ):
#     ...

# @app.command(help="Archive workflow")
# def archive(
#     id: Annotated[int, Argument(..., help="Workflow ID")]
# ):
#     ...

# @app.command(help="Delete workflow")
# def delete(
#     id: Annotated[int, Argument(..., help="Workflow ID")]
# ):
#     ...

