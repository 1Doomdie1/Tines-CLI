from rich    import print
from os.path import exists
from os      import makedirs

if __name__ == "__main__":    
    # Create .env file
    if not exists(".env"):
        print("[[bold green]+[/bold green]] Creating '.env' file")
        with open(".env", "w") as dotenv:
            dotenv.writelines(["TENANT_DOMAIN="])

    # Create tenants folder
    if not exists("tenants"):
        print("[[bold green]+[/bold green]] Creating 'tenants' folder")
        makedirs("tenants")
