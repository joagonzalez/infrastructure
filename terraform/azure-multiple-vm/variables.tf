variable "location" {}

variable "admin_username" {
  type        = string
  description = "Administrator user name for virtual machine"
}

variable "admin_password" {
  type        = string
  description = "Password must meet Azure complexity requirements"
}

variable "numbercount" {
    type 	  = number
    default       = 3
} 

variable "prefix" {
  type    = string
  default = "newcos"
}

variable "tags" {
  type = map

  default = {
    Environment = "Development"
    Dept        = "Research and Development"
    Team        = "DevOps"
  }
}

variable "sku" {
  default = {
    westus2 = "16.04-LTS"
    eastus  = "18.04-LTS"
  }
}

# network variables
variable "vnet_name" {
     description = "vnet for cluster"
     default     = "cluster_vnet"
}
variable "address_space" {
     default     = ["10.0.0.0/16"]
}
variable "subnet_name" {
     default     = "cluster_subnet"
}
variable "address_prefix" {
      default     = "10.0.1.0/24"
}