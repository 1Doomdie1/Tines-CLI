from rich.console                 import Console
from core.managers.tenant_manager import TenantManager

CONSOLE = Console(log_path=False)

class WorkflowManager:
    @staticmethod
    def create_workflow(
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

        req = TenantManager.enpoint_call(
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

        req = TenantManager.enpoint_call(
            "GET",
            "api/v1/stories",
            json=DATA
        )

        if req["status_code"] == 200:
            if not req["data"]["stories"]: CONSOLE.log("No workflows found"); exit()
            return req["data"]["stories"]

    @staticmethod
    def update(
        id:                     int,
        name:                   str, 
        description:            str,  
        add_tag_names:          str, 
        remove_tag_names:       str, 
        keep_events_for:        str, 
        disabled:               bool,
        locked:                 bool,
        priority:               bool,
        sts_access_source:      str, 
        sts_access:             str,
        shared_team_slugs:      str, 
        sts_skill_conf:         bool,
        entry_agent_id:         int,
        exit_agent_ids:         str,
        team_id:                int,
        folder_id:              int,
        change_control_enabled: bool
    ) -> None:
        optional_fields = {
            "locked":                 locked,
            "priority":               priority,
            "disabled":               disabled,
            "description":            description,
            "sts_skill_conf":         sts_skill_conf,
            "keep_events_for":        keep_events_for,
            "change_control_enabled": change_control_enabled
        }

        DATA = {
            "name":                   name,
            "add_tag_names":          add_tag_names.split(",") if add_tag_names else None, 
            "remove_tag_names":       remove_tag_names.split(",") if remove_tag_names else None, 
            "sts_access_source":      "SPECIFIC_TEAMS" if shared_team_slugs else sts_access_source, 
            "sts_access":             sts_access,
            "shared_team_slugs":      shared_team_slugs.split(",") if shared_team_slugs else [], 
            "entry_agent_id":         entry_agent_id,
            "exit_agent_ids":         exit_agent_ids.split(",") if exit_agent_ids else None,
            "team_id":                team_id,
            "folder_id":              folder_id,
            **{key: value for key, value in optional_fields.items() if value},
        }

        req = TenantManager.enpoint_call(
            "PUT",
            f"api/v1/stories/{id}",
            json=DATA
        )

        if req["status_code"] == 200:
            CONSOLE.log("Workflow has been updated succesfully")
        else:
            CONSOLE.log("Error encountered")
            CONSOLE.log("Message: [bold red]{}[/bold red]".format(req["data"][0]))