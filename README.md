# Tines-CLI 🚀  
A powerful CLI tool for managing workflows across multiple [Tines](https://www.tines.com/) tenants.  

---

## 📥 Installation  
1. **Clone the Repository**  
   ```bash
   $> git clone https://github.com/1Doomdie1/Tines-CLI
   $> cd tines-cli
   ```
2. **Install Dependencies**<br>
   ```bash
   $> pip install -r requirements.txt
   ```
3. **Set Up the CLI**
   ```bash
   $> pip install --editable .
   ```
## 🛠️ Capabilities  

<details>
<summary>Tenant Management</summary>


| **Command** | **Syntax**                                               | **Description**              |
|-------------|----------------------------------------------------------|------------------------------|
| `list`      | `tines tenant list`                                      | View all tenants.            |
| `info`      | `tines tenant info`                                      | Display tenant information.  |
| `delete`    | `tines tenant delete`                                    | Remove an existing tenant.   |
| `add`       | `tines tenant add --domain=<DOMAIN> --api-key=<API-key>` | Add a new tenant.            |
| `checkout`  | `tines tenant checkout --domain=<DOMAIN>`                | Switch to a specific tenant. |
</details>

<details>
<summary>Workflow Management</summary>

| **Command**    | **Syntax**                                              | **Description**                      |
|:---------------|---------------------------------------------------------|--------------------------------------|
| `list`         | `tines workflow list`                                   | View workflows.                      |
| `info`         | `tines workflow --wid=<ID> info`                        | Get details of a specific workflow.  |
| `create`       | `tines workflow create --name=<NAME> --team-id=<ID>`    | Create a new workflow.               |
| `update`       | `tines workflow --wid=<ID> update [OPTIONS]`            | Modify an existing workflow.         |
| `import`       | `tines workflow import --file=<PATH> --new-name=<NAME>` | Import a workflow to remote tenant.  |
| `export`       | `tines workflow export [OPTIONS]`                       | Export a workflow to a file.         |
| `delete`       | `tines workflow --wid=<ID> delete`                      | Remove a workflow.                   |
| `exports`      | `tines workflow exports`                                | Get a list of local exports.         |
| `batch-delete` | `tines workflow <IDS>`                                  | Delete multiple workflows in one go. |
</details>

<details>
<summary>Teams Management</summary>

| **Command** | **Syntax**                                      | **Description**      |
|:------------|-------------------------------------------------|----------------------|
| `list`      | `tines team list`                               | View teams.          |
| `info`      | `tines team --tid=<ID> info`                    | Get team details.    |
| `create`    | `tines team create <NAME>`                      | Create team.         |
| `update`    | `tines team --tid=<ID> update [OPTIONS]`        | Update team.         |
| `delete`    | `tines team --tid=<ID> delete`                  | Delete team.         |
| `member`    | `tines team --tid=<ID> member [OPTIONS] [ARGS]` | Manage team members. |
</details>

<details>
<summary>Members Management (Team)</summary>

| **Command** | **Syntax**                                            | **Description**           |
|:------------|-------------------------------------------------------|---------------------------|
| `list`      | `tines team --tid=<ID> member list`                   | View members of a team.   |
| `remove`    | `tines team --tid=<ID> member --uid=<ID> remove`      | Remove member from team.  |
| `invite`    | `tines team --tid=<ID> member invite --email=<EMAIL>` | Invite member to team.    |
</details>


## 🔗 Connecting to Your Tenant
**Things you'll need**:

- A [Tines API key](https://www.tines.com/api/authentication/)
- Your tenant's domain (part of the URL):
    ```
    URL    = https://<YOUR_TENANT_ID>.tines.com/
    DOMAIN = <YOUR_TENANT_ID>
    ```

**Add Tenant**
```bash
$> tines tenant add --domain=cool-domain-1234 --api-key=qwertyuio-123

[14:40:29] Tenant 'cool-domain-1234' added successfully  
```

**Set Default tenant**
```bash
$> tines tenant checkout cool-domain-1234

[14:40:29] Now using 'cool-domain-1234' tenant
```

**Quick way**
```bash
$> tines tenant add --domain=cool-domain-1234 --api-key=qwertyuio-123 --checkout

[14:40:29] Tenant 'cool-domain-1234' added successfully
           Now using 'cool-domain-1234' tenant
```


## ✍️ Creating a Workflow
To create a workflow, you'll need the `team_id`
1. **List Teams**
    ```bash
    $> tines team list

    ┏━━━━━━━┳━━━━━━━━━━━━━━━┓
    ┃  ID   ┃     Name      ┃
    ┡━━━━━━━╇━━━━━━━━━━━━━━━┩
    │ 12345 │ My Cool Team  │
    └───────┴───────────────┘
    ```
2. **Create Workflow**
    ```bash
    $> tines workflow create --name="My cool story name" --team-id=12345

    [14:45:44] Workflow 'My cool story name' has been created successfully  
               Link: https://cool-domain-1234.tines.com/stories/56789
    ```
## 📖 Help
At any point the `--help` flag can be used to show what `args`, `options` or `flags` can be used

## ❤️ Contributing
Contributions are welcome! Feel free to submit a pull request or raise an issue.

