from json              import dumps
from click             import Choice
from tapi              import StoriesAPI
from prettytable       import PrettyTable
from typer             import Typer, Context
from typing_extensions import Annotated, List
from typer             import Argument, Option


workflow_typer = Typer(name = "workflow", help = "Manage workflows")

OPTIONS = {
    "DOMAIN":  "",
    "API_KEY": "",
    "OUTPUT_FORMAT": [
        "json", "table"
    ],
    "FILTERS": [
        "SEND_TO_STORY_ENABLED", "HIGH_PRIORITY",
        "API_ENABLED", "PUBLISHED", "FAVORITE",
        "CHANGE_CONTROL_ENABLED", "DISABLED", "LOCKED"
    ],
    "ORDER": [
        "NAME", "NAME_DESC", "RECENTLY_EDITED",
        "LEAST_RECENTLY_EDITED", "ACTION_COUNT_ASC",
        "ACTION_COUNT_DESC"
    ]
}


@workflow_typer.command(name = "list", help = "Get a list of workflows")
def list_(
        team_id:   Annotated[int,       Option(..., help = "Team ID"                                                 )] = None,
        folder_id: Annotated[int,       Option(..., help = "Folder ID"                                               )] = None,
        per_page:  Annotated[int,       Option(..., help = "Number of results per request"                           )] = None,
        page:      Annotated[int,       Option(..., help = "Page number"                                             )] = None,
        tags:      Annotated[List[str], Option(..., help = "A comma separated list of tag names to filter by"        )] = None,
        filter:    Annotated[str,       Option(..., click_type  = Choice(OPTIONS["FILTERS"]),        help = "Filter results")] = None,
        order:     Annotated[str,       Option(..., click_type  = Choice(OPTIONS["ORDER"]),          help = "Order results" )] = None,
        output_as: Annotated[str,       Option(..., click_type  = Choice(OPTIONS["OUTPUT_FORMAT"]),  help = "Format results")] = "table"
):
    stories_api = StoriesAPI(OPTIONS["DOMAIN"], OPTIONS["API_KEY"])
    req = stories_api.list(team_id = team_id, folder_id = folder_id, per_page = per_page, page = page, tags = tags, filter = filter, order = order)
    status_code = req.get("status_code")

    if status_code == 200:
        stories = req.get("body").get("stories")
        if stories:
            if output_as == "table":
                table = PrettyTable()
                table.field_names = ["Nr", "ID", "Name", "Description", "Mode", "Folder ID", "Team ID", "Status", "Created At", "Updated At", "Edited At"]
                for index, story in enumerate(stories, 1):
                    table.add_row([
                        index,
                        story.get("id"),
                        story.get("name"),
                        f"{story.get("description")[:20]}..." if story.get("description") else None,
                        story.get("mode"),
                        story.get("folder_id"),
                        story.get("team_id"),
                        "Disabled" if not story.get("disabled") else "Enabled",
                        story.get("created_at"),
                        story.get("updated_at"),
                        story.get("edited_at")
                    ])
                print(table)
            else:
                print(dumps(stories, indent = 4))
        else:
            print("[-] No workflows found!")
    else:
        print(f"[!] Unable to pull workflows")
        print(f"    -> Status code: {status_code}")
        print(f"    -> Message: {req.get("body")}")


@workflow_typer.callback(invoke_without_command = True)
def callback(ctx: Context):
    OPTIONS["DOMAIN"]  = ctx.obj.get("DOMAIN")
    OPTIONS["API_KEY"] = ctx.obj.get("API_KEY")

    if ctx.command in ("list",) and not ctx.obj.get("DOMAIN") or not ctx.obj.get("API_KEY"):
        print("[-] You first need to checkout a tenant before using this command.")