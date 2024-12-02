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
   $> go install .
   ```
3. **Set Up the CLI**
    ### Windows
   ```bash
   $> go build -o tines.exe
   ```
   ### Linux
   ```bash
   $> go build -o tines
   ```
## 🛠️ Capabilities  

<details>
<summary>Tenant Management</summary>

| **Command** | **Syntax**                                  | **Description**              |
|-------------|-------------------------------------------- |------------------------------|
| `list`      | `tines tenant list`                         | View all tenants.            |
| `info`      | `tines tenant info`                         | Display tenant information.  |
| `add`       | `tines tenant add -d <DOMAIN> -a <API-key>` | Add a new tenant.            |
| `checkout`  | `tines tenant checkout -d <DOMAIN>`         | Switch to a specific tenant. |
</details>

<details>
<summary>Workflow Management</summary>

| **Command** | **Syntax**                                     | **Description**        |
|:------------|------------------------------------------------|------------------------|
| `list`      | `tines workflow list`                          | View workflows.        |
| `create`    | `tines workflow create -n <NAME> -t <TEAM ID>` | Create a new workflow. |
</details>

<details>
<summary>Teams Management</summary>

| **Command** | **Syntax**                                     | **Description** |
|:------------|------------------------------------------------|-----------------|
| `list`      | `tines team list`                              | View teams.     |
| `create`    | `tines team create -n <NAME>`                  | Create team.    |
| `update`    | `tines team -t <TEAM ID> update -n <NEW NAME>` | Update team.    |
</details>

<details>
<summary>Members Management (Team)</summary>

| **Command** | **Syntax**                                           | **Description**          |
|:------------|----------------------------------------------------- |------------------------- |
| `list`      | `tines team -t <TEAM ID> member list`                | View members of a team.  |
| `remove`    | `tines team -t <TEAM ID> member -u <USER ID> remove` | Remove member from team. |
| `invite`    | `tines team -t <TEAM ID> member invite -e <EMAIL>`   | Invite member to team.   |
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
$> tines tenant add -d cool-domain-1234 -a qwertyuio-123
```

**Set Default tenant**
```bash
$> tines tenant checkout cool-domain-1234
```

**Adding a tenant and checking it out**
```bash
$> tines tenant add -d cool-domain-1234 -a qwertyuio-123 -c
```

## 📖 Help
At any point the `-h` flag can be used to show what `args`, `options` or `flags` can be used

## ❤️ Contributing
Contributions are welcome! Feel free to submit a pull request or raise an issue.

