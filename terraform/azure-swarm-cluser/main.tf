# Configure the Microsoft Azure Provider.
terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 2.26"
    }
  }
}

provider "azurerm" {
  features {}
}

# Create a resource group
resource "azurerm_resource_group" "rg" {
  count = var.numbercount
  name     = "${var.prefix}-TFRG-${count.index}"
  location = var.location
  tags     = var.tags
}

# Create virtual network
resource "azurerm_virtual_network" "vnet" {
  name                = "${var.prefix}-TFVnet-${count.index}"
  address_space       = ["10.0.0.0/16"]
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = var.tags
}

# Create subnet
resource "azurerm_subnet" "subnet" {
  name                 = "${var.prefix}-TFSubnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes       = ["10.0.1.0/24"]
}

# Create public IP
resource "azurerm_public_ip" "publicip" {
  count               = var.numbercount
  name                = "${var.prefix}-TFPublicIP-${count.index}"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Dynamic"
  tags                = var.tags
}

# Create Network Security Group and rule
resource "azurerm_network_security_group" "nsg" {
  name                = "${var.prefix}-TFNSG"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = var.tags

  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

# Create network interface
resource "azurerm_network_interface" "nic" {
  count               = var.numbercount
  name                = "${var.prefix}NIC-${count.index}"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = var.tags

  ip_configuration {
    name                          = "${var.prefix}-NICConfg-${count.index}"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "dynamic"
    public_ip_address_id          = element(azurerm_public_ip.publicip.*.id, count.index)
  }
}

# Create a Linux virtual machine
resource "azurerm_virtual_machine" "vm" {
  count                 = var.numbercount
  name                  = "${var.prefix}-terraform-${count.index}"
  location              = var.location
  resource_group_name   = azurerm_resource_group.rg.name
  network_interface_ids = [element(azurerm_network_interface.nic.*.id, count.index)] 
  vm_size               = "Standard_DS1_v2"
  tags                  = var.tags

  storage_os_disk {
    name              = "${var.prefix}-OsDisk-${count.index}"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Premium_LRS"
    disk_size_gb      = "30"
  }

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = lookup(var.sku, var.location)
    version   = "latest"
  }

  os_profile {
    admin_username = var.admin_username
    admin_password = var.admin_password
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }

}

data "azurerm_public_ip" "ip" {
  name                = azurerm_public_ip.publicip.name
  resource_group_name = azurerm_virtual_machine.vm.resource_group_name
  depends_on          = [azurerm_virtual_machine.vm]
}

output "os_sku" {
  value = lookup(var.sku, var.location)
}

output "public_ip_address" {
  value = data.azurerm_public_ip.ip.ip_address
}