module "aws" {
  source	         = "./aws"
  aws_access_key     = "${var.aws_access_key}"
  aws_secret_key     = "${var.aws_secret_key}"
  region             = "${var.aws_region}"
  instance_type      = "${var.aws_instance_type}"
  key_path           = "${var.key_path}"
  public_key_path    = "${var.public_key_path}"
  key_name           = "${var.key_name}"
}

output "aws_tinia_ip" {
      value = "${module.aws.tinia_ip}"
}


