
.PHONY: galaxy get validate plan aws show destroy_aws init

galaxy:
	ansible-galaxy install -f -r ./requirements.yml

init:
	terraform init

get: init
	terraform get

validate: get
	terraform validate -var-file=terraform.tfvars

plan: validate
	terraform plan

show: plan
	terraform show

#AWS
aws: plan
	terraform apply -target=module.aws ; \
	terraform refresh

destroy_aws: validate
	terraform plan -destroy -target=module.aws ; terraform destroy -target=module.aws











