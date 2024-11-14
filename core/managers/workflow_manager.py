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
