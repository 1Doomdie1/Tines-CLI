from typing                       import List
from rich.console                 import Console
from core.managers.tenant_manager import TenantManager

CONSOLE = Console(log_path=False)

class TeamsManager:

    @staticmethod
    def create(
        name: str
    ) -> None:

        DATA = {
            "name": name
        }

        req = TenantManager.endpoint_call(
            "POST",
            "api/v1/teams",
            json=DATA
        )

        if req["status_code"] == 200:
            CONSOLE.log("Team created succesfully")
        else:
            CONSOLE.log("Error encountered")
            CONSOLE.log("Message: [bold red]{}[/bold red]".format(req["data"][0]))
    
    @staticmethod
    def get(
        team_id: int
    ) -> dict:
        
        DATA = {
            "team_id": team_id
        }

        req = TenantManager.endpoint_call(
            "GET",
            f"api/v1/teams/{team_id}",
            json=DATA
        )

        if req["status_code"] == 200:
            return req["data"]
        else:
            CONSOLE.log("Error encountered")
            CONSOLE.log("Message: [bold red]{}[/bold red]".format(req["data"][0]))
            exit()
    
    @staticmethod
    def list(
        include_drafts: bool
    ) -> list:
        
        DATA = {
            "include_drafts": include_drafts,
            "per_page": 500
        }

        req = TenantManager.endpoint_call(
            "GET",
            "api/v1/teams",
            json=DATA
        )

        if req["status_code"] == 200:
            return req["data"]["teams"]
        else:
            CONSOLE.log("Error encountered")
            CONSOLE.log("Message: [bold red]{}[/bold red]".format(req["data"][0]))
            exit()

    @staticmethod
    def update(
        team_id: int,
        name:    str,
    ) -> None:
        
        DATA = {
            "name": name
        }

        req = TenantManager.endpoint_call(
            "PUT",
            f"api/v1/teams/{team_id}",
            json=DATA
        )

        if req["status_code"] == 200:
            CONSOLE.log("Team name updated successfully")
        else:
            CONSOLE.log("Error encountered")
            CONSOLE.log("Message: [bold red]{}[/bold red]".format(req["data"][0]))

    @staticmethod
    def members(
        team_id: int
    ) -> List:

        DATA = {
            "per_page": 500
        }

        req = TenantManager.endpoint_call(
            "GET",
            f"api/v1/teams/{team_id}/members",
            json=DATA
        )

        if req["status_code"] == 200:
            return req["data"]["members"]
        else:
            CONSOLE.log("Error encountered")
            CONSOLE.log("Message: [bold red]{}[/bold red]".format(req["data"][0]))
            exit()

    @staticmethod
    def remove_member(
        team_id: int,
        user_id: int
    ) -> None:

        DATA = {
            "user_id": user_id
        }

        req = TenantManager.endpoint_call(
            "POST",
            f"api/v1/teams/{team_id}/remove_member",
            json=DATA
        )

        if req["status_code"] == 200:
            CONSOLE.log("Member removed successfully")
        else:
            CONSOLE.log("Error encountered")
            CONSOLE.log("Message: [bold red]{}[/bold red]".format(req["data"][0]))

    @staticmethod
    def delete(
        team_id: int,
    ) -> None:
        answer = input("Are you sure you want to delete this team? (y/n): ")

        if answer.strip() == "y":
            req = TenantManager.endpoint_call(
                "DELETE",
                f"api/v1/teams/{team_id}/remove_member"
            )

            if req["status_code"] == 204:
                CONSOLE.log("Team deleted successfully")
            else:
                CONSOLE.log("Error encountered")
                CONSOLE.log("Message: [bold red]{}[/bold red]".format(req["data"][0]))
        elif answer.strip() in ("n", ""):
            CONSOLE.log("Aborted")

    @staticmethod
    def invite_member(
        team_id: int,
        email:   str,
        user_id: int,
        role:    str
    ) -> None:

        OPTIONAL_FLAGS = {
            "email":   email,
            "user_id": user_id
        }

        DATA = {
            "role": role,
            **{key: value for key, value in OPTIONAL_FLAGS.items() if value != None}
        }

        req = TenantManager.endpoint_call(
            "POST",
            f"api/v1/teams/{team_id}/invite_member",
            json=DATA
        )

        if req["status_code"] == 200:
            CONSOLE.log("Invite sent")
        else:
            CONSOLE.log("Error encountered")
            CONSOLE.log("Message: [bold red]{}[/bold red]".format(req["data"][0]))
