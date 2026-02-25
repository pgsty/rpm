#==============================================================#
# File      :   terraform.tf
# Desc      :   5-node oss building env for x86_64/aarch64
# Ctime     :   2024-12-12
# Mtime     :   2026-01-16
# Path      :   tf/terraform
# License   :   AGPLv3 @ https://pigsty.io/docs/about/license
# Copyright :   2018-2025  Ruohang Feng / Vonng (rh@vonng.com)
#==============================================================#


#===========================================================#
# Architecture, Instance Type, OS Images
#===========================================================#
locals {
  bandwidth = 100                       # internet bandwidth in Mbps (100Mbps)
  disk_size = 100                       # system disk size in GB (100GB)
  spot_policy = "SpotAsPriceGo"                # NoSpot, SpotWithPriceLimit, SpotAsPriceGo
  spot_price_limit = 5                  # only valid when spot_policy is SpotWithPriceLimit
  instance_type_map = {
    amd64 = "ecs.c9i.2xlarge"
    arm64 = "ecs.c8y.2xlarge"
  }
  amd64_instype = local.instance_type_map["amd64"]
  arm64_instype = local.instance_type_map["arm64"]
}

data "alicloud_images" "el8_amd64_img" {
  owners     = "system"
  name_regex = "^rockylinux_8_10_x64"
}
data "alicloud_images" "el8_arm64_img" {
  owners     = "system"
  name_regex = "^rockylinux_8_10_arm64"
}
data "alicloud_images" "el9_amd64_img" {
  owners     = "system"
  name_regex = "^rockylinux_9_7_x64"
}
data "alicloud_images" "el9_arm64_img" {
  owners     = "system"
  name_regex = "^rockylinux_9_7_arm64"
}
data "alicloud_images" "el10_amd64_img" {
  owners     = "system"
  name_regex = "^rockylinux_10_1_x64"
}
data "alicloud_images" "el10_arm64_img" {
  owners     = "system"
  name_regex = "^rockylinux_10_1_arm64"
}

#===========================================================#
# Credentials
#===========================================================#
# add your credentials here or pass them via env
# export ALICLOUD_ACCESS_KEY="????????????????????"
# export ALICLOUD_SECRET_KEY="????????????????????"
# e.g : ./aliyun-key.sh
provider "alicloud" {
  # access_key = "????????????????????"
  # secret_key = "????????????????????"
  region = "cn-shanghai"
}


#===========================================================#
# VPC, SWITCH, SECURITY GROUP
#===========================================================#
# use 10.10.10.0/24 cidr block as demo network
resource "alicloud_vpc" "vpc" {
  vpc_name   = "pigsty-net"
  cidr_block = "10.10.10.0/24"
}

# add virtual switch for pigsty demo network
resource "alicloud_vswitch" "vsw" {
  vpc_id     = "${alicloud_vpc.vpc.id}"
  cidr_block = "10.10.10.0/24"
  zone_id    = "cn-shanghai-l"
}

# add default security group and allow all tcp traffic
resource "alicloud_security_group" "default" {
  security_group_name   = "default"
  vpc_id = "${alicloud_vpc.vpc.id}"
}
resource "alicloud_security_group_rule" "allow_all_tcp" {
  ip_protocol       = "tcp"
  type              = "ingress"
  nic_type          = "intranet"
  policy            = "accept"
  port_range        = "1/65535"
  priority          = 1
  security_group_id = "${alicloud_security_group.default.id}"
  cidr_ip           = "0.0.0.0/0"
}



#======================================#
# EL8 AMD64
#======================================#
resource "alicloud_instance" "pg-el8" {
  instance_name                 = "pg-el8"
  host_name                     = "pg-el8"
  private_ip                    = "10.10.10.8"
  instance_type                 = local.amd64_instype
  image_id                      = "${data.alicloud_images.el8_amd64_img.images.0.id}"
  vswitch_id                    = "${alicloud_vswitch.vsw.id}"
  security_groups               = ["${alicloud_security_group.default.id}"]
  password                      = "PigstyDemo4"
  instance_charge_type          = "PostPaid"
  internet_charge_type          = "PayByTraffic"
  spot_strategy                 = local.spot_policy
  spot_price_limit              = local.spot_price_limit
  internet_max_bandwidth_out    = local.bandwidth
  system_disk_category          = "cloud_essd"
  system_disk_performance_level = "PL1"
  system_disk_size              = local.disk_size
}

output "el8_ip" {
  value = "${alicloud_instance.pg-el8.public_ip}"
}


#======================================#
# EL8 ARM64
#======================================#
resource "alicloud_instance" "pg-el8a" {
  instance_name                 = "pg-el8a"
  host_name                     = "pg-el8a"
  private_ip                    = "10.10.10.108"
  instance_type                 = local.arm64_instype
  image_id                      = "${data.alicloud_images.el8_arm64_img.images.0.id}"
  vswitch_id                    = "${alicloud_vswitch.vsw.id}"
  security_groups               = ["${alicloud_security_group.default.id}"]
  password                      = "PigstyDemo4"
  instance_charge_type          = "PostPaid"
  internet_charge_type          = "PayByTraffic"
  spot_strategy                 = local.spot_policy
  spot_price_limit              = local.spot_price_limit
  internet_max_bandwidth_out    = local.bandwidth
  system_disk_category          = "cloud_essd"
  system_disk_performance_level = "PL1"
  system_disk_size              = local.disk_size
}

output "el8a_ip" {
  value = "${alicloud_instance.pg-el8a.public_ip}"
}


#======================================#
# EL9 AMD64
#======================================#
resource "alicloud_instance" "pg-el9" {
  instance_name                 = "pg-el9"
  host_name                     = "pg-el9"
  private_ip                    = "10.10.10.9"
  instance_type                 = local.amd64_instype
  image_id                      = "${data.alicloud_images.el9_amd64_img.images.0.id}"
  vswitch_id                    = "${alicloud_vswitch.vsw.id}"
  security_groups               = ["${alicloud_security_group.default.id}"]
  password                      = "PigstyDemo4"
  instance_charge_type          = "PostPaid"
  internet_charge_type          = "PayByTraffic"
  spot_strategy                 = local.spot_policy
  spot_price_limit              = local.spot_price_limit
  internet_max_bandwidth_out    = local.bandwidth
  system_disk_category          = "cloud_essd"
  system_disk_performance_level = "PL1"
  system_disk_size              = local.disk_size
}

output "el9_ip" {
  value = "${alicloud_instance.pg-el9.public_ip}"
}



#======================================#
# EL9 ARM64
#======================================#
resource "alicloud_instance" "pg-el9a" {
  instance_name                 = "pg-el9a"
  host_name                     = "pg-el9a"
  private_ip                    = "10.10.10.109"
  instance_type                 = local.arm64_instype
  image_id                      = "${data.alicloud_images.el9_arm64_img.images.0.id}"
  vswitch_id                    = "${alicloud_vswitch.vsw.id}"
  security_groups               = ["${alicloud_security_group.default.id}"]
  password                      = "PigstyDemo4"
  instance_charge_type          = "PostPaid"
  internet_charge_type          = "PayByTraffic"
  spot_strategy                 = local.spot_policy
  spot_price_limit              = local.spot_price_limit
  internet_max_bandwidth_out    = local.bandwidth
  system_disk_category          = "cloud_essd"
  system_disk_performance_level = "PL1"
  system_disk_size              = local.disk_size
}

output "el9a_ip" {
  value = "${alicloud_instance.pg-el9a.public_ip}"
}


#======================================#
# EL10 AMD64
#======================================#
resource "alicloud_instance" "pg-el10" {
  instance_name                 = "pg-el10"
  host_name                     = "pg-el10"
  private_ip                    = "10.10.10.10"
  instance_type                 = local.amd64_instype
  image_id                      = "${data.alicloud_images.el10_amd64_img.images.0.id}"
  vswitch_id                    = "${alicloud_vswitch.vsw.id}"
  security_groups               = ["${alicloud_security_group.default.id}"]
  password                      = "PigstyDemo4"
  instance_charge_type          = "PostPaid"
  internet_charge_type          = "PayByTraffic"
  spot_strategy                 = local.spot_policy
  spot_price_limit              = local.spot_price_limit
  internet_max_bandwidth_out    = local.bandwidth
  system_disk_category          = "cloud_essd"
  system_disk_performance_level = "PL1"
  system_disk_size              = local.disk_size
}

output "el10_ip" {
  value = "${alicloud_instance.pg-el10.public_ip}"
}


#======================================#
# EL10 ARM64
#======================================#
resource "alicloud_instance" "pg-el10a" {
  instance_name                 = "pg-el10a"
  host_name                     = "pg-el10a"
  private_ip                    = "10.10.10.110"
  instance_type                 = local.arm64_instype
  image_id                      = "${data.alicloud_images.el10_arm64_img.images.0.id}"
  vswitch_id                    = "${alicloud_vswitch.vsw.id}"
  security_groups               = ["${alicloud_security_group.default.id}"]
  password                      = "PigstyDemo4"
  instance_charge_type          = "PostPaid"
  internet_charge_type          = "PayByTraffic"
  spot_strategy                 = local.spot_policy
  spot_price_limit              = local.spot_price_limit
  internet_max_bandwidth_out    = local.bandwidth
  system_disk_category          = "cloud_essd"
  system_disk_performance_level = "PL1"
  system_disk_size              = local.disk_size
}

output "el10a_ip" {
  value = "${alicloud_instance.pg-el10a.public_ip}"
}


# sshpass -p PigstyDemo4 ssh-copy-id el8
# sshpass -p PigstyDemo4 ssh-copy-id el9
# sshpass -p PigstyDemo4 ssh-copy-id el10

# sshpass -p PigstyDemo4 ssh-copy-id el8a
# sshpass -p PigstyDemo4 ssh-copy-id el9a
# sshpass -p PigstyDemo4 ssh-copy-id el10a

