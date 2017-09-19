# terraform-tinia
Terraform to deploy Tinia in Clouds

## Usage
+ rename terraform.tfvars.example to terraform.tfvars and fill-in AWS credentials
+ ./setup.py aws                       - deploy VM to EC2 AWS
+ ./setup.py destroy_aws               - destroy EC2 AWS resources
+ http://{aws_tinia_ip}/trell/static/  - tinia web interface (Re)start master job
