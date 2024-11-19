from core.utils.types           import *
from rich.table                 import Table
from typing_extensions          import Annotated
from core.managers.team_manager import TeamsManager
from core.commands.member       import list_members
from core.commands.member       import app as member_app
from typer                      import Typer, Argument, Option, Context, Exit


app = Typer()
app.add_typer(member_app)

@app.callback()
def manage_team_flags(
    ctx: Context,
    tid: int = Option(None, help="Team ID"),
) -> None:
    ctx.obj["tid"] = tid
    console = ctx.obj.get("console")

    if ctx.invoked_subcommand in {"info", "update", "delete", "member"} and tid is None:
        console.log("Error: --tid is required for this command.")
        console.log("Usage: tines team --tid=<ID> (info | udpate | delete | member)")
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
    console = ctx.obj.get("console")

    team_info = TeamsManager.get(tid)
    
    if format_as == Output_Format_Types.TABLE:
        console.print(f"[bold]Team ID:[/bold] {team_info['id']}")
        console.print(f"[bold]Team Name:[/bold] {team_info['name']}\n")

        if team_info['groups']:
            table = Table(title="Groups", title_justify="left")
            table.add_column("Group ID",   justify="center")
            table.add_column("Group Name", justify="center")

            for group in team_info['groups']:
                table.add_row(str(group['id']), group['name'])
            console.print(table)
        else:
            console.log("No groups")
    elif format_as == Output_Format_Types.JSON:
        console.print(team_info)

    if include_members:
            print("\n")
            list_members(format_as, ctx)

@app.command(help="List teams", name="list")
def _list(
    include_drafts: Annotated[bool,                Option(..., help="Include draft teams in the response")] = False,
    format_as:      Annotated[Output_Format_Types, Option(..., help="Output format"                      )] = Output_Format_Types.TABLE,
    ctx:            Context                                                                                 = Context
) -> None:
    console = ctx.obj.get("console")
    teams = TeamsManager.list(include_drafts)

    if format_as == Output_Format_Types.TABLE:
        table = Table(title="Teams", title_justify="left")
        table.add_column("ID",   justify="center")
        table.add_column("Name", justify="center")

        for team in teams:
            table.add_row(f'{team["id"]}', team["name"])
        console.print(table)
    elif format_as == Output_Format_Types.JSON:
        console.print(teams)

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
