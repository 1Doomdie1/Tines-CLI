from core.utils.types           import *
from rich.table                 import Table
from rich.console               import Console
from typing_extensions          import Annotated
from core.managers.team_manager import TeamsManager
from core.commands.member       import list_members
from core.commands.member       import app as member_app
from typer                      import Typer, Argument, Option, Context, Exit


app = Typer()
app.add_typer(member_app)

CONSOLE = Console(log_path=False)

@app.callback()
def manage_team_flags(
    ctx: Context,
    tid: int = Option(None, help="Team ID"),
) -> None:
    ctx.obj = {"tid": tid}

    if ctx.invoked_subcommand in {"info", "update", "delete", "member"} and tid is None:
        CONSOLE.log("Error: --tid is required for this command.")
        CONSOLE.log("Usage: tines team --tid=<ID> (info | udpate | delete | member)")
        raise Exit(1)


@app.command(help="Create new team")
def create(
    name: Annotated[str, Argument(..., help="Team name")]
) -> None:
    TeamsManager.create(name)

@app.command(help="Get team info")
def info(
    include_members: Annotated[bool,                Option  (..., help="Show team members")] = False,
    format_as:       Annotated[Output_Format_Types, Option  (..., help="Output format"    )] = Output_Format_Types.TABLE,
    ctx:             Context                                                                 = Context
) -> None:
    tid = ctx.obj.get("tid")
    TEAM_INFO = TeamsManager.get(tid)
    
    if format_as == Output_Format_Types.TABLE:
        CONSOLE.print(f"[bold]Team ID:[/bold] {TEAM_INFO['id']}")
        CONSOLE.print(f"[bold]Team Name:[/bold] {TEAM_INFO['name']}\n")

        if TEAM_INFO['groups']:
            TABLE = Table(title="Groups", title_justify="left")
            TABLE.add_column("Group ID",   justify="center")
            TABLE.add_column("Group Name", justify="center")

            for group in TEAM_INFO['groups']:
                TABLE.add_row(str(group['id']), group['name'])
            CONSOLE.print(TABLE)
        else:
            CONSOLE.log("No groups")
    elif format_as == Output_Format_Types.JSON:
        CONSOLE.print(TEAM_INFO)

    if include_members:
            print("\n")
            list_members(format_as)

@app.command(help="List teams", name="list")
def _list(
    include_drafts: Annotated[bool,                Option(..., help="Include draft teams in the response")] = False,
    format_as:      Annotated[Output_Format_Types, Option(..., help="Output format"                      )] = Output_Format_Types.TABLE
) -> None:
    TEAMS = TeamsManager.list(include_drafts)

    if format_as == Output_Format_Types.TABLE:
        TABLE = Table(title="Teams", title_justify="left")
        TABLE.add_column("ID",   justify="center")
        TABLE.add_column("Name", justify="center")

        for team in TEAMS:
            TABLE.add_row(f'{team["id"]}', team["name"])
        CONSOLE.print(TABLE)
    elif format_as == Output_Format_Types.JSON:
        CONSOLE.print(TEAMS)

@app.command(help="Update team")
def update(
    name: Annotated[str, Option(..., help="New team name")],
    ctx:  Context = Context
) -> None:
    TeamsManager.update(ctx.obj.get("tid"), name)

@app.command(help="Delete team (Dangerous!!!)")
def delete(
    ctx: Context = Context
) -> None:
    TeamsManager.delete(ctx.obj.get("tid"))
