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
# Capabilities
- Tenant Management
  - add
  - delete
  - checkout
  - teams
  - info
  - list

- Workflow Management
  - create
  - list

# How to connect to your tenant
For this you will need a [tines api key](https://www.tines.com/api/authentication/) and your tenant domain. To get your tenant domain just login to tines and copy this part of the url `https://<YOUR_TENANT_ID>.tines.com/`.
```
URL    = https://cool-domain-1234.tines.com/
DOMAIN = cool-domain-1234
```
Now you can run this command
```
$> tines tenant add cool-domain-1234 qwertyuio-123 --checkout
                          ^              ^              ^
                          |              |              |
                        Domain        API Key    Use this tenant by default

[14:40:29] Tenant 'cool-domain-1234' added successfully
           Now using 'cool-domain-1234' tenant
```

To get tenat info use this command
```
$> tines tenant info
┏━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Name ┃  Type  ┃  Region   ┃  Egress IPs   ┃
┡━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ eu2  │ shared │ eu-west-1 │ 10.10.101.110 │
│      │        │           │ 20.20.202.220 │
└──────┴────────┴───────────┴───────────────┘
```

For more information on what commands you can use please use the `--help` flag
```
$> tines --help
$> tines tenant --help
$> tines tenant add --help
```

# Creating a workflow
To create a workflow you will need the `team_id` which can be obtained like so
```
$> tines tenant teams
┏━━━━━━━┳━━━━━━━━━━━━━━━┓
┃  ID   ┃     Name      ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━┩
│ 12345 │ Forensics Lab │
└───────┴───────────────┘
```

Now use the following command
```
$> tines workflow create "My cool story name" --team-id=12345

[14:45:44] Workflow 'My cool story name' has been created succesfully
           Link: https://cool-domain-1234.tines.com/stories/56789
```