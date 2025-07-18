from typing            import List
from click             import Choice
from os.path           import join
from typing_extensions import Annotated
from prettytable       import PrettyTable
from typer             import Typer, Context
from typer             import Option, Argument
from json              import dumps, dump, load
from tapi              import StoriesAPI, EventsAPI, RunsAPI, ActionsAPI

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
    "WORKFLOW_ID": None,
    "AGENT_TYPE": [
        "Agents::EmailAgent", "Agents::EventTransformationAgent",
        "Agents::HTTPRequestAgent", "Agents::IMAPAgent",
        "Agents::TriggerAgent", "Agents::WebhookAgent",
        "Agents::SendToStoryAgent", "Agents::GroupAgent",
        "Agents::FormAgent", " Agents::HTTPRequestAgent",
        "Agents::LLMAgent", "Agents::RunScriptAgent"
    ],
    "ENTRY_TYPE": [ "entry", "transit", "exit" ],
    "EXPORTS_FOLDER": None,
    "IMPORT_MODES": [ "new", "versionReplace" ]
}


@workflow_typer.command(name = "list", help = "Get a list of workflows")
def list_(
        team_id:   Annotated[int,       Option(..., help = "Team ID"                                                      )] = None,
        folder_id: Annotated[int,       Option(..., help = "Folder ID"                                                    )] = None,
        per_page:  Annotated[int,       Option(..., help = "Number of results per request"                                )] = None,
        page:      Annotated[int,       Option(..., help = "Page number"                                                  )] = None,
        tags:      Annotated[List[str], Option(..., help = "A comma separated list of tag names to filter by"             )] = None,
        filter:    Annotated[str,       Option(..., help = "Filter results", click_type = Choice(OPTIONS["FILTERS"])      )] = None,
        order:     Annotated[str,       Option(..., help = "Order results",  click_type = Choice(OPTIONS["ORDER"])        )] = None,
        output_as: Annotated[str,       Option(..., help = "Format results", click_type = Choice(OPTIONS["OUTPUT_FORMAT"]))] = "table"
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
                table.align["Name"] = "l"
                table.align["Description"] = "l"

                for index, story in enumerate(stories, 1):
                    table.add_row([
                        index,
                        story.get("id"),
                        story.get("name") if len(story.get("name")) <= 20 else f"{story.get("name")[:20]}...",
                        f"{story.get("description")[:20]}{"..." if len(story.get("description")) >= 20 else ""}" if story.get("description") else "[ N/A ]",
                        story.get("mode"),
                        story.get("folder_id"),
                        story.get("team_id"),
                        "Disabled" if story.get("disabled") else "Enabled",
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

@workflow_typer.command(help = "Pull a list of events from a workflow")
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
                prev_ev_ids = tuple(map(str, event.get("previous_events_ids")))
                prev_ev_ids = "\n".join([", ".join(prev_ev_ids[index:index+4]) for index in range(0, len(prev_ev_ids), 4)])
                table.add_row([
                    index,
                    event.get("id"),
                    event.get("agent_id"),
                    event.get("story_run_guid"),
                    prev_ev_ids,
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

@workflow_typer.command(name = "event", help = "Get a workflow event")
def event_(
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
    else:
        print(f"[!] Error encountered")
        print(f"    -> Status code: {status_code}")
        print(f"    -> Message: {req.get("body")}")


@workflow_typer.command(name = "runs", help = "Get a list of workflow runs")
def runs_(
    story_mode: Annotated[str, Option(..., help = "Story mode", click_type = Choice(["LIVE", "TEST"])                )] = None,
    draft_id:   Annotated[int, Option(..., help = "Return runs for a specific draft"                                 )] = None,
    since:      Annotated[str, Option(..., help = "Only retrieve story runs that started after this time"            )] = None,
    until:      Annotated[str, Option(..., help = "Only retrieve story runs that started until this time"            )] = None,
    output_as:  Annotated[str, Option(..., help = "Format results", click_type  = Choice(OPTIONS["OUTPUT_FORMAT"])   )] = "table",
    per_page:   Annotated[int, Option(..., help = "Set the number of results returned per page"                      )] = 20,
    page:       Annotated[int, Option(..., help = "Specify the page of results to return if there are multiple pages")] = 1,
):
    runs_api = RunsAPI(OPTIONS["DOMAIN"], OPTIONS["API_KEY"])
    req = runs_api.list(story_id = OPTIONS["WORKFLOW_ID"], story_mode = story_mode, draft_id = draft_id, since = since, until = until, per_page = per_page, page = page)
    status_code = req.get("status_code")
    runs = req.get("body", {}).get("story_runs")

    if status_code == 200:

        if not runs:
            print("[!] Story has not runs")
            exit()

        if output_as == "table":
            table = PrettyTable()
            table.field_names = [ "Nr", "GUID", "Story Mode", "Duration (s)", "Action Count", "Event Count", "Started At", "Ended At" ]

            for index, run in enumerate(runs):
                table.add_row([
                    index,
                    run.get("guid"),
                    run.get("story_mode"),
                    run.get("duration"),
                    run.get("action_count"),
                    run.get("event_count"),
                    run.get("start_time"),
                    run.get("end_time")
                ])
            print(table)
        else:
            print(dumps(runs, indent = 4))
    else:
        print(f"[!] Error encountered")
        print(f"    -> Status code: {status_code}")
        print(f"    -> Message: {req.get("body")}")

@workflow_typer.command(name = "actions", help = "Get a list of actions")
def actions_(
        story_mode:  Annotated[str,       Option(..., help = "Story mode", click_type = Choice(["live", "test"])                           )] = None,
        team_id:     Annotated[int,       Option(..., help = "List actions for the given team"                                             )] = None,
        group_id:    Annotated[int,       Option(..., help = "List actions for the given group"                                            )] = None,
        entry_type:  Annotated[List[str], Option(..., help = "Sort by entry type", click_type= Choice(OPTIONS["ENTRY_TYPE"])               )] = None,
        action_type: Annotated[str,       Option(..., help = "Filter actions by the given type", click_type = Choice(OPTIONS["AGENT_TYPE"]))] = None,
        draft_id:    Annotated[int,       Option(..., help = "Return runs for a specific draft"                                            )] = None,
        output_as:   Annotated[str,       Option(..., help = "Format results", click_type=Choice(OPTIONS["OUTPUT_FORMAT"])                 )] = "table",
        per_page:    Annotated[int,       Option(..., help = "Set the number of results returned per page"                                 )] = 20,
        page:        Annotated[int,       Option(..., help = "Specify the page of results to return if there are multiple pages"           )] = 1
):
    actions_api = ActionsAPI(OPTIONS["DOMAIN"], OPTIONS["API_KEY"])
    req = actions_api.list(
        story_id = OPTIONS["WORKFLOW_ID"], story_mode = story_mode,
        team_id = team_id, group_id = group_id, action_type = action_type,
        draft_id = draft_id, per_page = per_page,page = page
    )

    status_code = req.get("status_code")
    actions = req.get("body").get("agents")

    if status_code == 200:

        if entry_type:
            entry_types = {
                "entry": lambda a: not a.get("sources"),
                "transit": lambda a: a.get("sources") and a.get("receivers"),
                "exit": lambda a: a.get("sources") and not a.get("receivers"),
            }
            actions = [action for action in actions if any(entry_types[ent](action) for ent in entry_type)]

        if output_as == "table":
            table = PrettyTable(
                [
                    "ID", "Type", "Name", "Description", "Source Actions",
                    "Receiver Actions", "Entry Type", "Last Ran At"
                ]
            )

            table.align["Source Actions"] = "l"
            table.align["Receiver Actions"] = "l"
            table.align["Type"] = "l"
            table.align["Name"] = "l"

            for action in actions:
                sources   = "\n".join([f"{action.get("sources")[index: index + 4]}" for index in range(0, len(action.get("sources")), 4)])
                receivers = "\n".join([f"{action.get("receivers")[index: index + 4]}" for index in range(0, len(action.get("receivers")), 4)])

                table.add_row(
                    [
                        action.get("id"),
                        action.get("type"),
                        f"{action.get("name")[:20]}..." if len(action.get("name")) >= 20 else action.get("name"),
                        f"{action.get("description")[:20]}{"..." if len(action.get("description")) >= 20 else ""}" if action.get("description") else "[ N/A ]",
                        sources,
                        receivers,
                        "Entry" if not sources else "Transit" if sources and receivers else "Exit",
                        action.get("last_event_at"),
                    ],
                )

            print(table.get_string(sortby="Entry Type", ))
            print(
                f"|  Page: {page}  |  Page Size: {per_page}  "
                f"|  Total Pages: {req.get("body").get("meta").get("pages")}  "
                f"|  Total Actions: {req.get("body").get("meta").get("count")}  |"
            )
        elif output_as == "json":
            print(dumps(actions, indent=4))

@workflow_typer.command(help = "Disable story")
def disable():
    story_api = StoriesAPI(OPTIONS["DOMAIN"], OPTIONS["API_KEY"])
    req = story_api.disable(id = OPTIONS["WORKFLOW_ID"], disabled = True)
    status_code = req.get("status_code")

    if status_code == 200:
        print("[+] Story successfully disabled")
    else:
        print(f"[!] Error encountered")
        print(f"    -> Status code: {status_code}")
        print(f"    -> Message: {req.get("body")}")


@workflow_typer.command(help = "Enable story")
def enable():
    story_api = StoriesAPI(OPTIONS["DOMAIN"], OPTIONS["API_KEY"])
    req = story_api.disable(id = OPTIONS["WORKFLOW_ID"], disabled = False)
    status_code = req.get("status_code")

    if status_code == 200:
        print("[+] Story successfully enabled")
    else:
        print(f"[!] Error encountered")
        print(f"    -> Status code: {status_code}")
        print(f"    -> Message: {req.get("body")}")

@workflow_typer.command(help = "Export workflow")
def export(
        path:           Annotated[str,  Option(..., help = "Export path"                   )] = None,
        randomize_urls: Annotated[bool, Option(..., help = "Randomize pages urls."         )] = None,
        draft_id:       Annotated[int,  Option(..., help = "The ID of the draft to export.")] = None
):
    story_api = StoriesAPI(OPTIONS["DOMAIN"], OPTIONS["API_KEY"])
    req = story_api.export(OPTIONS["WORKFLOW_ID"], randomize_urls = randomize_urls, draft_id = draft_id)
    status_code = req.get("status_code")
    story = req.get("body")
    path = path if path else join(OPTIONS["EXPORTS_FOLDER"], f"{story.get("slug")}.json")

    if status_code == 200:
        with open(path, "w") as file:
            dump(story, file, indent = 4)
        print("[+] Story exported successfully")
        print(f"    -> {path}")
    else:
        print(f"[!] Error encountered")
        print(f"    -> Status code: {status_code}")
        print(f"    -> Message: {req.get("body")}")

@workflow_typer.command(name = "import", help = "Import workflow")
def import_(
        name:      Annotated[str,  Argument(..., help = "The new name for the story"                                                                 )],
        path:      Annotated[str,  Argument(..., help = "Path to story"                                                                              )],
        team_id:   Annotated[int,  Argument(..., help = "ID of team to which the story should be added"                                              )],
        folder_id: Annotated[int,  Option  (..., help = "ID of folder to which the story should be added"                                            )] = None,
        mode:      Annotated[str,  Option  (..., help = "Create a new story or update existing by Name", click_type = Choice(OPTIONS["IMPORT_MODES"]))] = "new",
):
    try:
        with open(path, "r") as file:
            story_data = load(file)
    except Exception as e:
        print(f"[!] Error encountered")
        print(f"    -> Message: {e}")
        exit()

    story_api = StoriesAPI(OPTIONS["DOMAIN"], OPTIONS["API_KEY"])
    req = story_api.import_(new_name = name, data = story_data, team_id = team_id, folder_id = folder_id, mode = mode)
    status_code = req.get("status_code")

    if status_code == 200:
        print("[+] Story imported successfully")
    else:
        print(f"[!] Error encountered")
        print(f"    -> Status code: {status_code}")
        print(f"    -> Message: {req.get("body")}")

@workflow_typer.command(help = "Delete workflow")
def delete():
    story_api = StoriesAPI(OPTIONS["DOMAIN"], OPTIONS["API_KEY"])
    req = story_api.delete(story_id = OPTIONS["WORKFLOW_ID"])
    status_code = req.get("status_code")

    if status_code == 204:
        print("[+] Story deleted successfully")
    else:
        print(f"[!] Error encountered")
        print(f"    -> Status code: {status_code}")
        print(f"    -> Message: {req.get("body")}")

@workflow_typer.callback()
def callback(
        ctx: Context,
        wid: Annotated[int, Option(..., help = "Workflow ID")] = None
):
    OPTIONS["DOMAIN"]         = ctx.obj.get("DOMAIN")
    OPTIONS["API_KEY"]        = ctx.obj.get("API_KEY")
    OPTIONS["EXPORTS_FOLDER"] = ctx.obj.get("EXPORTS_FOLDER")

    if not ctx.obj.get("DOMAIN") or not ctx.obj.get("API_KEY"):
        print("[-] You first need to checkout a tenant before using this command.")
        exit()

    if ctx.invoked_subcommand not in ("list", "import") and not wid:
        print("[-] Please provide the a workflow ID")
        print(f"    -> tines workflow --wid=<ID> {ctx.invoked_subcommand} (args) [flags] <switches>")
        exit()

    OPTIONS["WORKFLOW_ID"] = wid
