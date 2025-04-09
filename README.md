# Tines-CLI

## About
Tines-CLI is a simple command line tool designed to manage your [Tines](https://www.tines.com/) tenants.
This project's core module is [tapi](https://github.com/1Doomdie1/tapi), a simple module built as a wrapper for the Tines REST API.

## Installation
```commandline
$> pip install git+https://github.com/1Doomdie1/Tines-CLI
```

## Getting started

### Add tenant
```commandline
$> tines tenant add domain=my-tines-domain api_key=me_secret_key

[+] Tenant my-tines-domain has been added successfully
``` 

### Checkout tenant
```commandline
$> tines tenant checkout --domain=my-tines-domain

[+] Now using the 'my-tines-domain' tenant
```

### Tenant Info
```commandline
$> tines tenant info

+------+--------+-----------+-----------------------------+
| Name |  Type  |   Region  |          Egress IPs         |
+------+--------+-----------+-----------------------------+
| us1  | shared | us-west-2 |  10.10.10.10, 10.10.10.11   |
+------+--------+-----------+-----------------------------+
```

### Find out more.
At any point you can use the `--help` flag and get information on what commands/args/options you have access to, so don't hesitate to use it.

## Upcoming Updates

### Adding the following commands:

#### Tenant
- [ ] tines tenant logs
- [ ] tines tenant invite
- [ ] tines tenant remove-member

#### Workflows
- [ ] tines workflow get
- [ ] tines workflow list
- [ ] tines workflow logs
- [ ] tines workflow import
- [ ] tines workflow export

#### Teams
- [ ] tines team add
- [ ] tines team list
- [ ] tines team delete
- [ ] tines team invite
- [ ] tines team remove
- [ ] tines team set-name

### Improvements

- Standardizing error output
- Code cleanup
- Better documentation