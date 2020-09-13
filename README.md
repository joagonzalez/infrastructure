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
    - [azure-multiple-vm](#azure-multiple-vm)
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
Ansible playbooks for different functions

- greenfield linux: dispatcher that enables different tasks for different function like banner config, apt repositories config, docker install, telegraf install, etc
- ping_monitoring: Parsing icmp output with textFSM and writing that information to influxDB in order to monitor latency
- sbc: Gather informartion and parsing data with textFSM to monitor session border controller through telent

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

### azure-multiple-vm
Deploy N vms in azure setting parameterz like number of instances to deploy, network, subnet, etc.

## Docker
Dockerfile and docker-compose files for multiples services

- Jenkins
- Harbor docker registry
- Apache airflow
- NGINX + GeoIP
- portainer.io
- prometheus
- sftp server
- telemetry (influxdb + grafana)

## Examples

## References
