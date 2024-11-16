from pathlib                      import Path
from rich.console                 import Console
from core.managers.tenant_manager import TenantManager
from json                         import load, JSONDecodeError

CONSOLE = Console(log_path=False)

class WorkflowManager:
    @staticmethod
    def create(
        team_id:         str,
        name:            str,
        description:     str,
        keep_events_for: str,
        folder_id:       int,
        tags:            str,
        disabled:        bool,
        priority:        bool
    ) -> None:
        TIME_PERIODS = {
            "1h":   3600,
            "6h":   21600,
            "1d":   86400,
            "3d":   259200,
            "7d":   604800,
            "14d":  1209600,
            "30d":  2592000,
            "60d":  5184000,
            "90d":  7776000,
            "180d": 15552000,
            "365d": 31536000,
        }

        DATA = {
            "team_id":         team_id,
            "name":            name,
            "description":     description,
            "keep_events_for": TIME_PERIODS[keep_events_for],
            "folder_id":       folder_id,
            "tags":            tags.split(",") if tags else None,
            "disabled":        disabled,
            "priority":        priority
        }

        req = TenantManager.endpoint_call(
            "POST",
            "api/v1/stories",
            json=DATA
        )

        if req["status_code"] == 201:
            CONSOLE.log(f"Workflow '{name}' has been created succesfully")
            CONSOLE.log(f'Link: https://{TenantManager.tenant_data()["domain"]}.tines.com/stories/{req["data"]["id"]}')
        else:
            CONSOLE.log("Error encountered")
            CONSOLE.log(f'Message: [bold red]{req["data"][0]}[/bold red]')
        return

    @staticmethod
    def list_workflows(
        team_id:   int,
        folder_id: int,
        per_page:  int,
        page:      int,
        tags:      str,
        filter:    str,
        order:     str
    ) -> list:
        
        DATA = {
            "team_id":   team_id,
            "folder_id": folder_id,
            "per_page":  per_page,
            "page":      page,
            "tags":      tags,
            "filter":    filter,
            "order":     order
        }

        req = TenantManager.endpoint_call(
            "GET",
            "api/v1/stories",
            json=DATA
        )

        if req["status_code"] == 200:
            if not req["data"]["stories"]: CONSOLE.log("No workflows found"); exit()
            return req["data"]["stories"]

    @staticmethod
    def update(
        id: int,
        name, 
        description, 
        add_tag_names,
        remove_tag_names, 
        keep_events_for, 
        disabled, 
        locked,
        priority, 
        sts_access_source, 
        sts_access, 
        shared_team_slugs,
        sts_skill_conf, 
        entry_agent_id, 
        exit_agent_ids, team_id,
        folder_id, 
        change_control_enabled
    ) -> dict:
        DATA = locals()

        DATA.update({
            "add_tag_names":     add_tag_names.split(",") if add_tag_names else None,
            "remove_tag_names":  remove_tag_names.split(",") if remove_tag_names else None,
            "sts_access_source": "SPECIFIC_TEAMS" if shared_team_slugs and not sts_access_source else sts_access_source,
            "shared_team_slugs": shared_team_slugs.split(",") if shared_team_slugs else None,
            "exit_agent_ids":    exit_agent_ids.split(",") if exit_agent_ids else None,
        })

        DATA = {key: value for key, value in DATA.items() if value != None}

        if  len(DATA) == 1: CONSOLE.log("At least one option needs to be specified. Please use the '--help' flag"); exit()

        req = TenantManager.endpoint_call(
            "PUT",
            f"api/v1/stories/{id}",
            json=DATA
        )

        if req["status_code"] == 200:
            CONSOLE.log("Workflow has been updated succesfully")
            del DATA["id"]
            return DATA

        CONSOLE.log("Error encountered")
        CONSOLE.log("Message: [bold red]{}[/bold red]".format(req["data"][0]))
        exit()

    @staticmethod
    def get(
        id:   int,
        mode: str
    ) -> dict:
        
        DATA = {
            "story_id":   id,
            "story_mode": mode 
        }

        req = TenantManager.endpoint_call(
            "GET",
            f"api/v1/stories/{id}",
            json=DATA
        )

        if req["status_code"] == 200:
            return req["data"]

        CONSOLE.log("Error encountered")
        CONSOLE.log("Message: [bold red]{}[/bold red]".format(req["data"][0]))
        exit()
    
    @staticmethod
    def delete(
        id: int
    ) -> None:

        DATA = {
            "story_id": id
        }

        req = TenantManager.endpoint_call(
            "DELETE",
            f"api/v1/stories/{id}",
            json=DATA
        )

        if req["status_code"] == 204:
            CONSOLE.log("Workflow deleted succesfully")
        else:
            CONSOLE.log("Error encountered")
            CONSOLE.log("Message: [bold red]{}[/bold red]".format(req["data"][0]))

    @staticmethod
    def batch_delete(
        ids: list
    ) -> None:

        DATA = {
            "ids": ids
        }

        req = TenantManager.endpoint_call(
            "DELETE",
            "api/v1/stories/batch",
            json=DATA
        )

        if req["status_code"] == 204:
            CONSOLE.log("Workflows deleted succesfully")
        else:
            CONSOLE.log("Error encountered")
            CONSOLE.log("Message: [bold red]{}[/bold red]".format(req["data"][0]))

    @staticmethod
    def export(
        id:             int,
        randomize_urls: bool
    ) -> dict:

        DATA = {
            "randomize_urls": randomize_urls
        }

        req = TenantManager.endpoint_call(
            "GET",
            f"api/v1/stories/{id}/export",
            json=DATA
        )

        if req["status_code"] == 200:
            return req["data"]
        else:
            CONSOLE.log("Error encountered")
            CONSOLE.log("Message: [bold red]{}[/bold red]".format(req["data"][0]))
            exit()

    @staticmethod
    def _import(
        file:      Path,
        new_name:  str,
        team_id:   int,
        folder_id: int,
        mode:      str
    ) -> None:
        try:
            with open(file, "r") as file:
                STORY_DATA = load(file)

            OPTIONAL_FLAGS = {
                "folder_id": folder_id,
            }

            DATA = {
                "data": STORY_DATA,
                "new_name": new_name,
                "team_id": team_id,
                "mode": mode,
                **{key: value for key, value in OPTIONAL_FLAGS.items() if value != None}
            }

            req = TenantManager.endpoint_call(
                "POST",
                f"api/v1/stories/import",
                json=DATA
            )

            if req["status_code"] == 200:
                CONSOLE.log("Workflow has been imported successfully")
            else:
                CONSOLE.log("Error encountered")
                CONSOLE.log("Message: [bold red]{}[/bold red]".format(req["data"][0]))
        except JSONDecodeError:
            CONSOLE.log("Error encountered")
            CONSOLE.log(f"Message: [bold red]Invalid workflow format. File format must be json and not emplty.[/bold red]")
        except FileNotFoundError as e:
            CONSOLE.log("Error encountered")
            CONSOLE.log(f"Message: [bold red]{e}[/bold red]")
