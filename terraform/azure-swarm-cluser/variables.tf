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