from core.utils.types           import *
from rich.table                 import Table
from rich.console               import Console
from core.managers.team_manager import TeamsManager
from typing_extensions          import Annotated, List
from typer                      import Typer, Argument, Option, prompt

app = Typer()

CONSOLE = Console(log_path=False)

@app.command(help="Create new team")
def create(
    name: Annotated[str, Argument(..., help="Team name")]
) -> None:
    TeamsManager.create(name)

@app.command(help="Get team info")
def info(
    team_id:         Annotated[int,                 Argument(..., help="Team ID"          )],
    include_members: Annotated[bool,                Option  (..., help="Show team members")] = False,
    format_as:       Annotated[Output_Format_Types, Option  (..., help="Output format"    )] = Output_Format_Types.TABLE
) -> None:
    TEAM_INFO = TeamsManager.get(team_id)
    
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
            members(team_id, format_as)

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
    team_id: Annotated[int, Argument(..., help="Team ID"      )],
    name:    Annotated[str, Option  (..., help="New team name")],
) -> None:
    TeamsManager.update(team_id, name)

@app.command(help="Delete team (Dangerous!!!)")
def delete(
    team_id: Annotated[int, Argument(..., help="Team ID")]
) -> None:
    TeamsManager.delete(team_id)

@app.command(help="Get team members")
def members(
    team_id:   Annotated[int,                 Argument(..., help="Team ID"      )],
    format_as: Annotated[Output_Format_Types, Option  (..., help="Output format")] = Output_Format_Types.TABLE
) -> None:
    MEMBERS = TeamsManager.members(team_id)

    if format_as == Output_Format_Types.TABLE:
        TABLE = Table(title="Members", title_justify="left")
        
        for column in MEMBERS[0].keys():
            TABLE.add_column(column.capitalize().replace("_", " "))

        for member in MEMBERS:
            TABLE.add_row(
                f'{member["id"]}', member["first_name"], member["last_name"],
                member["email"], f'{member["is_admin"]}', member["created_at"],
                member["last_seen"], f'{member["invitation_accepted"]}', member["role"]
            )
        CONSOLE.print(TABLE)
    elif format_as == Output_Format_Types.JSON:
        CONSOLE.print(MEMBERS)

@app.command(help="Remove member from team")
def remove_member(
    user_id: Annotated[int, Argument(..., help="User ID")],
    team_id: Annotated[int, Option  (..., help="Team ID")]
) -> None:
    TeamsManager.remove_member(team_id, user_id)

@app.command(help="Invite member to team")
def invite_member(
    team_id: Annotated[int,               Argument(..., help="Team ID"   )],
    email:   Annotated[str | None,        Option  (..., help="User email")] = None,
    user_id: Annotated[int | None,        Option  (..., help="User ID"   )] = None,
    role:    Annotated[Team_Member_Types, Option  (..., help="Team ID"   )] = Team_Member_Types.VIEWER
) -> None:
    if email and user_id:
        CONSOLE.log("Please specify either the 'email' or 'user_id' not both")
        exit()
    elif not email and not user_id:
        CONSOLE.log("'email' or 'user_id' must be specified")
        exit()

    TeamsManager.invite_member(team_id, email, user_id, role)
