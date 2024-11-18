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


| **Command**   | **Description**                        |
|---------------|----------------------------------------|
| `add`         | Add a new tenant.                      |
| `delete`      | Remove an existing tenant.             |
| `checkout`    | Switch to a specific tenant.           |
| `info`        | Display tenant information.            |
| `list`        | View all tenants.                      |
</details>

<details>
<summary>Workflow Management</summary>

| **Command**    | **Description**                      |
|:---------------|--------------------------------------|
| `list`         | View workflows.                      |
| `info`         | Get details of a specific workflow.  |
| `create`       | Create a new workflow.               |
| `update`       | Modify an existing workflow.         |
| `import`       | Import a workflow to remote tenant.  |
| `export`       | Export a workflow to a file.         |
| `delete`       | Remove a workflow.                   |
| `exports`      | Get a list of local exports.         |
| `batch-delete` | Delete multiple workflows in one go. |
</details>

<details>
<summary>Teams Management</summary>

| **Command**      | **Description**           |
|:-----------------|---------------------------|
| `list`           | View teams.               |
| `info`           | Get team details.         |
| `create`         | Create team.              |
| `update`         | Update team.              |
| `delete`         | Delete team.              |
| `member`         | Manage team members.      |
</details>

<details>
<summary>Members Management (Team)</summary>

| **Command**      | **Description**           |
|:-----------------|---------------------------|
| `list`           | View members of a team.   |
| `remove`         | Remove member from team.  |
| `invite`         | Invite member to team.    |
</details>


## 🔗 Connecting to Your Tenant
**Things you'll need**:

- A [Tines API key](https://www.tines.com/api/authentication/)
- Your tenant's domain (part of the URL):
    ```
    URL    = https://<YOUR_TENANT_ID>.tines.com/
    DOMAIN = <YOUR_TENANT_ID>
    ```

**Add and Set a Default Tenant**
```bash
$> tines tenant add cool-domain-1234 qwertyuio-123 --checkout

[14:40:29] Tenant 'cool-domain-1234' added successfully  
           Now using 'cool-domain-1234' tenant
```
**Output**


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
    $> tines workflow create "My cool story name" --team-id=12345

    [14:45:44] Workflow 'My cool story name' has been created successfully  
               Link: https://cool-domain-1234.tines.com/stories/56789
    ```
## 📖 Help
At any point the `--help` flag can be used to show what `args`, `options` or `flags` can be used

## ❤️ Contributing
Contributions are welcome! Feel free to submit a pull request or raise an issue.

