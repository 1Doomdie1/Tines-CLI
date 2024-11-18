from core.utils.types           import *
from rich.table                 import Table
from rich.console               import Console
from typing_extensions          import Annotated
from core.managers.team_manager import TeamsManager
from typer                      import Typer, Context, Option, Argument, Exit


CONSOLE = Console(log_path=False)

app = Typer(name="member", help="Manage team members")

@app.callback()
def manage_member_flags(
    ctx: Context,
    uid: int = Option(None, help="User ID"),
) -> None:
    ctx.obj["uid"] = uid

    if ctx.invoked_subcommand in {"info", "remove"} and uid is None:
        CONSOLE.log("Error: --uid is required for this command.")
        CONSOLE.log("Usage: team --tid=<ID> member --uid=<ID> (info | remove)")
        raise Exit(1)


@app.command(help="Get team members", name="list")
def list_members(
    format_as: Annotated[Output_Format_Types, Option  (..., help="Output format")] = Output_Format_Types.TABLE,
    ctx:       Context                                                             = Context
) -> None:
    MEMBERS = TeamsManager.members(ctx.obj.get("tid"))

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

@app.command(name = "remove", help="Remove member from team")
def remove_member(
    ctx: Context = Context
) -> None:
    TeamsManager.remove_member(ctx.obj.get("tid"), ctx.obj.get("uid"))

@app.command(name = "invite", help="Invite member to team")
def invite_member(
    email:   Annotated[str | None,        Option(..., help="User email")],
    role:    Annotated[Team_Member_Types, Option(..., help="Team ID"   )] = Team_Member_Types.VIEWER,
    ctx: Context = Context
) -> None:
    TeamsManager.invite_member(ctx.obj.get("tid"), email, role)
