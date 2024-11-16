from typing       import Union
from os           import scandir
from rich.console import Console
from os           import makedirs, remove
from json         import dump, load, loads
from os.path      import join, exists, abspath
from dotenv       import set_key, dotenv_values
from requests     import get, post, put, delete, RequestException

CONSOLE          = Console(log_path=False)
DOTENV_FILE      = abspath(".env")
TENANT_DIRECTORY = abspath("tenants")

# Create tenant folder if it doesn't exist
makedirs(TENANT_DIRECTORY, exist_ok=True)

# Create .env file if it doesn't exist
if not exists(DOTENV_FILE):
    with open(DOTENV_FILE, "w"):
        set_key(DOTENV_FILE, "USE_TENANT", "None")

class TenantManager:

    @staticmethod
    def add_tenant(
        domain:    str,
        api_key:   str,
        checkout:  bool = False,
        overwrite: bool = False
    ) -> None:
        TENANT_CONFIG_FILE_PATH = join(TENANT_DIRECTORY, f"{domain}.json")

        if exists(TENANT_CONFIG_FILE_PATH) and not overwrite: CONSOLE.log(f"Tenant '{domain}' already exists"); return

        if not TenantManager.validate_credentials(domain, api_key): CONSOLE.log(f"Invalid credentials"); return 

        with open(TENANT_CONFIG_FILE_PATH, "w") as file:
            dump({"domain": domain, "api_key": api_key}, file, indent=4)
        CONSOLE.log(f"Tenant '{domain}' added successfully")

        if checkout:
            TenantManager.checkout_tenant(domain)

    @staticmethod
    def checkout_tenant(
        domain: str
    ) -> None:
        TENANT_CONFIG_FILE_PATH = join(TENANT_DIRECTORY, f"{domain}.json")

        if not exists(TENANT_CONFIG_FILE_PATH): CONSOLE.log(f"Unknow tenant: '{domain}'"); return

        set_key(DOTENV_FILE, "USE_TENANT", domain)
        CONSOLE.log(f"Now using '{domain}' tenant")

    @staticmethod
    def delete_tenant() -> None:
        DOMAIN                  = TenantManager.tenant_data()["domain"]
        TENANT_CONFIG_FILE_PATH = join(TENANT_DIRECTORY, f"{DOMAIN}.json")

        TenantManager.checkout_tenant("None")
        set_key(DOTENV_FILE, "USE_TENANT", "None")
        remove(TENANT_CONFIG_FILE_PATH)

    @staticmethod
    def validate_credentials(
        domain:  str,
        api_key: str
    ) -> bool:
        request = get(f"https://{domain}.tines.com/api/v1/info", headers={"Authorization": f"Bearer {api_key}"})
        if request.status_code != 200: 
            return False
        return True

    @staticmethod
    def tenant_data() -> dict:
        domain = dotenv_values(DOTENV_FILE).get("USE_TENANT")
        if domain == "None": CONSOLE.log("No tenant selected. Please use the 'checkout' command"); exit()

        TENANT_CONFIG_FILE_PATH = join(TENANT_DIRECTORY, f"{domain}.json")
        with open(TENANT_CONFIG_FILE_PATH, "r") as file:
            return load(file)

    @staticmethod
    def tenant_teams() -> list:
        return TenantManager.endpoint_call(
            "GET",
            "api/v1/teams"
        )["data"]["teams"]

    @staticmethod
    def list_local_tenants() -> list:
        TENANTS = [tenant.name for tenant in scandir(TENANT_DIRECTORY) if tenant.is_file()]

        if not TENANTS: CONSOLE.log("No local tenants please use the 'tines tenant add' command to add one"); exit()

        return TENANTS

    @staticmethod
    def endpoint_call(
        method:   str,
        endpoint: str,
        params:   Union[str | None] = None,
        **kwargs
    ) -> Union[ dict | None]:
        METHODS = {
            "get":  get,
            "post": post,
            "put":  put,
            "delete":  delete
        }

        TENANT_DATA = TenantManager.tenant_data()
        URL = f"https://{TENANT_DATA['domain']}.tines.com/{endpoint}{f'?{params}' if params else ''}"

        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {TENANT_DATA['api_key']}"
        kwargs["headers"] = headers

        try:
            req = METHODS[method.lower()](URL, **kwargs)
            return {
                "data":        loads(req.content) if req.content else {},
                "status_code": req.status_code
            }
        except RequestException as e:
            CONSOLE.log(f"Request error encountered\n{e}")
        except KeyError:
            CONSOLE.log(f"Unknown HTTP method: [bold red]{method}[/bold red]")