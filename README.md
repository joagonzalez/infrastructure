# Infrastructure as Code
![Python](https://img.shields.io/badge/infrastructure-v1.0.0-orange)
![Python](https://img.shields.io/badge/ansible-v2.9.6-blue)
![Python](https://img.shields.io/badge/terraform-0.11.11-blue)
![Python](https://img.shields.io/badge/docker-v19.03.8-blue)
![Python](https://img.shields.io/badge/platform-linux--64%7Cwin--64-lightgrey)

Infrastructure as code templates using Terraform, Ansible, Docker, TextFSM, Jinja2. Templates are organised in differents folder by *technology/usecase*.

Usecases will be explained later on this readme file.


**Content**

- [Ansible](#ansible)
- [Terraform](#terraform)
    - [azure-vm](#azure-vm)
- [Docker](#docker)
- [Examples](#examples)
- [References](#references)


## Getting started

Dir structure of repo
```
.
├── ansible
├── doc
├── docker
├── scripts
└── terraform


5 directories
```

## Ansible

## Terraform
Basic commands
```
terraform init
terraform plan
terraform apply
terraform destroy
```
### azure-vm
Create a linux vm in Microsoft Azure with all requirements and parametrization through variables. IP address and vm sku are outputs of terraform task.

```
terraform plan -var "admin_password=Argentina_2020#" -var "admin_username=newcos"
terraform apply -var "admin_password=Argentina_2020#" -var "admin_username=newcos"
terraform destroy -var "admin_password=Argentina_2020#" -var "admin_username=newcos"
```
## Docker

## Examples

## References
