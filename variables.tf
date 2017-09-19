variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "aws_region" { default = "us-east-1" }
variable "aws_instance_type" { default = "t2.medium" }

variable "key_name" { default = "default" }
variable "public_key_path" { default = "./sshkeys/default.pub" }
variable "key_path" { default = "./sshkeys/default" }
variable "ssh_key_ID" { default = "4c:f5:cf:43:80:13:a4:3d:1f:4d:9d:b6:07:db:75:87" }
