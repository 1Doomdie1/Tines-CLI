# Tines-CLI

## About
Tines-CLI is a simple command line tool designed to manage your [Tines](https://www.tines.com/) tenants.
This project's core module is [tapi](https://github.com/1Doomdie1/tapi), a simple module built as a wrapper for the Tines REST API.

## Installation
```commandline
$> pip install git+https://github.com/1Doomdie1/Tines-CLI
```
## Update tines-cli

```commandline
$> tines utils update
```
## Getting started

### Add tenant
```commandline
$> tines tenant add my-tines-domain my_secret_key

[+] Tenant my-tines-domain has been added successfully
``` 

### Checkout tenant
```commandline
$> tines tenant checkout my-tines-domain

[+] Successfully checked out tenant 'my-tines-domain'
```

### Tenant Info
```commandline
$> tines tenant info

+-----------------+---------+--------+-----------+-----------------------------+
|      Domain     | SV Name |  Type  |   Region  |          Egress IPs         |
+-----------------+---------+--------+-----------+-----------------------------+
| my-tines-domain |   us1   | shared | us-west-2 |  10.10.10.10, 10.10.10.11   |
+-----------------+---------+--------+-----------+-----------------------------+
```

### List all tenant saved locally
```commandline
$> tines tenant list

+----+------------------+--------+
| Nr |      Domain      | In use |
+----+------------------+--------+
| 1  |  my-cool-domain  |   ✗    |
| 2  |  my-tines-domain |   ✓    |
+----+------------------+--------+
```
### Find out more.
At any point you can use the `--help` flag and get information on what commands/args/options you have access to, so don't hesitate to use it.

## Upcoming Updates

### Adding the following commands:

#### Utils
- [x] tines utils uninstall
- [x] tines utils update
- [x] tines utils versions
- [x] tines utils envars

#### Tenant

- [x] tines tenant add \[DOMAIN\] \[API_KEY\]
- [x] tines tenant checkout \[DOMAIN\]
- [x] tines tenant info
- [x] tines tenant list
- [x] tines tenant delete \[DOMAIN\]
- [ ] tines tenant invite \[EMAIL\]
- [ ] tines tenant remove-member \[USER_ID\]

#### Workflows
- [x] tines workflow list
- [x] tines workflow --wid=\[WORKFLOW_ID\] events
- [x] tines workflow --wid=\[WORKFLOW_ID\] event
- [x] tines workflow --wid=\[WORKFLOW_ID\] runs
- [x] tines workflow --wid=\[WORKFLOW_ID\] actions
- [x] tines workflow --wid=\[WORKFLOW_ID\] disable
- [x] tines workflow --wid=\[WORKFLOW_ID\] enable
- [x] tines workflow import \[NAME\] \[PATH/TO/JSON\] \[TEAM_ID\]
- [x] tines workflow --wid=\[WORKFLOW_ID\] export
- [x] tines workflow --wid=\[WORKFLOW_ID\] delete

#### Teams
- [ ] tines team add [TEAM_NAME\]
- [ ] tines team list
- [ ] tines team delete \[TEAM_ID\]
- [ ] tines team --tid=\[TEAM_ID\] invite \[EMAIL\]
- [ ] tines team --tid=\[TEAM_ID\] remove \[USER_ID\]
- [ ] tines team --tid=\[TEAM_ID\] set-name \[NEW_NAME\]

### Improvements

- Standardizing error output
- Code cleanup
- Better documentation