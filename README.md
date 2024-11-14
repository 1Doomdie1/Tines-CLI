# Tines-CLI
CLI tool to manage workflows across multiple Tines tenants.

# Instalation
After cloning the repository please install the `requirements` using the following command
```bash
pip install requirements.txt
```

After the requirements are installed please run the `setup.py` script
```bash
pip install --editable .
```

# How to connect to your tenant
For this you will need a [tines api key](https://www.tines.com/api/authentication/) and your tenant domain. To get your tenant domain just login to tines and copy this part of the url `https://<YOUR_TENANT_ID>.tines.com/`.
```
URL    = https://cool-domain-1234.tines.com/
DOMAIN = cool-domain-1234
```
Now you can run this command
```
tines tenant add cool-domain-1234 qwertyuio-123 --checkout
                       ^              ^              ^
                       |              |              |
                     Domain        API Key    Use this tenant by default
```

To get tenat info use this command
```
tines tenant info
```

For more information on what commands you can use please use the `--help` flag
```
tines --help
tines tenant --help
tines tenant add --help
```