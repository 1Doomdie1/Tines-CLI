from typing            import List
from json              import dumps
from click             import Choice
from typer             import Option
from typing_extensions import Annotated
from prettytable       import PrettyTable
from typer             import Typer, Context
from tapi              import StoriesAPI, EventsAPI


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
    ],
    "WORKFLOW_ID": None
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
        print(f"[!] Error encountered")
        print(f"    -> Status code: {status_code}")
        print(f"    -> Message: {req.get("body")}")

@workflow_typer.command(help = "Pull a list of events")
def events(
        since_id:       Annotated[int,  Option(..., help = "Only retrieve events after this ID"                                                    )] = None,
        until_id:       Annotated[int,  Option(..., help = "Only retrieve events until (and including) this ID."                                   )] = None,
        team_id:        Annotated[int,  Option(..., help = "Filter by the given team."                                                             )] = None,
        action_id:      Annotated[int,  Option(..., help = "Filter on action ID"                                                                   )] = None,
        since:          Annotated[str,  Option(..., help = "Only retrieve events created after this time (ISO 8601 timestamp)"                     )] = None,
        until:          Annotated[str,  Option(..., help = "Only retrieve events until this time (ISO 8601 timestamp)"                             )] = None,
        guid:           Annotated[str,  Option(..., help = "Filter on story GUID"                                                                  )] = None,
        include_groups: Annotated[bool, Option(..., help = "Include events from groups in the specified story. Only valid if story_id is specified")] = False,
        output_as:      Annotated[str,  Option(..., help = "Format output", click_type = Choice(OPTIONS["OUTPUT_FORMAT"])                          )] = "table",
        per_page:       Annotated[int,  Option(..., help = "Set the number of results returned per page"                                           )] = 20,
        page:           Annotated[int,  Option(..., help = "Specify the page of results to return if there are multiple pages"                     )] = 1,
):
    events_api = EventsAPI(OPTIONS["DOMAIN"], OPTIONS["API_KEY"])
    req = events_api.list(
        since_id = since_id, until_id = until_id, since = since,
        until = until, team_id = team_id, story_id = OPTIONS["WORKFLOW_ID"],
        include_groups = include_groups, per_page = per_page, page = page
    )

    status_code = req.get("status_code")
    w_events = req.get("body", {}).get("events", [])

    if not w_events:
        print("[-] No events found for this story")
        exit()

    if status_code == 200:
        w_events = [event for event in w_events if event.get("story_run_guid") == guid] if guid else w_events
        w_events = [event for event in w_events if event.get("agent_id") == action_id] if action_id else w_events

        if output_as == "table":
            table = PrettyTable()
            table.field_names = ["Nr", "Event ID", "Action ID", "Story GUID", "Previous Events IDS", "Created At", "Updated AT"]
            table.align["Previous Events IDS"] = "l"

            for index, event in enumerate(w_events, 1):
                table.add_row([
                    index,
                    event.get("id"),
                    event.get("agent_id"),
                    event.get("story_run_guid"),
                    ", ".join([f"{i}" for i in event.get("previous_events_ids")]),
                    event.get("created_at"),
                    event.get("updated_at")
                ])
            print(table)
            print(f"|  Page: {page}  |  Page Size: {per_page}  |  Total Pages: {req.get("body").get("meta").get("pages")}  |  Total Events: {req.get("body").get("meta").get("count")}  |")
        else:
            print(dumps(w_events, indent = 4))
    else:
        print(f"[!] Error encountered")
        print(f"    -> Status code: {status_code}")
        print(f"    -> Message: {req.get("body")}")

@workflow_typer.command(help = "Get an event")
def event(
        eid:  Annotated[int, Option(..., help = "Event ID")]
):
    events_api = EventsAPI(OPTIONS["DOMAIN"], OPTIONS["API_KEY"])
    req = events_api.get(event_id = eid)
    status_code = req.get("status_code")
    event = req.get("body", {})

    if status_code == 200:
        keys = event.get("payload").keys()
        longest_key = max((len(key) for key in keys))
        box_width = max(longest_key, 54) + (18 if longest_key > 54 else 0)
        margin_offset = box_width - 18

        print(f"┌{"─" * box_width}┐")
        print(f"│ ID:             {event.get("id"):<{margin_offset}} │")
        print(f"│ Agent ID:       {event.get("agent_id"):<{margin_offset}} │")
        print(f"│ Created At:     {event.get("created_at"):<{margin_offset}} │")
        print(f"│ Updated At:     {event.get("updated_at"):<{margin_offset}} │")
        print(f"│ Story Run GUID: {event.get("story_run_guid"):<{margin_offset}} │")
        print("│ Event Objects:  ", end="")

        for index, obj in enumerate(keys, 1):
            print(f"{obj:<{margin_offset}} │")
            if index < len(keys):
                print(f"│{" " * 17}", end="")

        print(f"└{"─" * box_width}┘")

@workflow_typer.callback()
def callback(
        ctx: Context,
        wid: Annotated[int, Option(..., help = "Workflow ID")] = None
):
    OPTIONS["DOMAIN"]  = ctx.obj.get("DOMAIN")
    OPTIONS["API_KEY"] = ctx.obj.get("API_KEY")

    if ctx.invoked_subcommand in ("list", "event", "events") and not ctx.obj.get("DOMAIN") or not ctx.obj.get("API_KEY"):
        print("[-] You first need to checkout a tenant before using this command.")
        exit()

    if ctx.invoked_subcommand in ("event", "events") and not wid:
        print("[-] Please provide the a workflow ID")
        print(f"    -> tines workflow --id=<ID> {ctx.invoked_subcommand} (args) [flags] <switches>")
        exit()

    OPTIONS["WORKFLOW_ID"] = wid