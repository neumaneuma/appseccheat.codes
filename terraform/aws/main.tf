terraform {
  backend "s3" {
    bucket         = "terraform-state-fd98f914-e3a3-e024-c533-fb339fbb5be3"
    key            = "state/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-locks"
  }
}

# Default provider configuration
provider "aws" {
  region = var.region
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

# S3 bucket names must be globally unique, so we use a random UUID to generate a unique name
resource "random_uuid" "uuid" {}

data "http" "cloudflare_ips" {
  url = "https://api.cloudflare.com/client/v4/ips"
}

locals {
  cloudflare_ipv4_addresses = jsondecode(data.http.cloudflare_ips.response_body).result.ipv4_cidrs
}

module "cloudtrail" {
  source      = "../modules/cloudtrail"
  region      = var.region
  trail_name  = "permissions-audit-trail"
  bucket_name = "cloudtrail-audit-logs-${random_uuid.uuid.result}"
}

module "certificates" {
  source          = "../modules/certificates"
  domain_name     = var.domain_name
  api_domain_name = var.api_domain_name
  region          = var.region
}

module "vpc" {
  source = "../modules/vpc"
  region = var.region
}

module "ecs" {
  source                                 = "../modules/ecs"
  region                                 = var.region
  rds_instance_url                       = module.database.db_host
  db_password                            = var.db_password
  bucket_name                            = "ecs-logs-${random_uuid.uuid.result}"
  public_subnet_ids                      = module.vpc.public_subnets[*].id
  private_subnet_ids                     = module.vpc.private_subnets[*].id
  public_subnet_cidr_blocks              = module.vpc.public_subnets[*].cidr_block
  private_subnet_cidr_blocks             = module.vpc.private_subnets[*].cidr_block
  docker_hub_repo                        = var.docker_hub_repo
  vpc_id                                 = module.vpc.vpc_id
  backend_cloudwatch_log_group_name      = var.backend_cloudwatch_log_group_name
  internal_api_cloudwatch_log_group_name = var.internal_api_cloudwatch_log_group_name
  ec2_host_name                          = var.ec2_host_name
  db_security_group_id                   = module.database.db_security_group_id
  cloudflare_ipv4_addresses              = local.cloudflare_ipv4_addresses
  origin_certificate                     = module.certificates.origin_certificate
  private_key_pem                        = module.certificates.private_key_pem
}

module "database" {
  source                     = "../modules/database"
  region                     = var.region
  vpc_id                     = module.vpc.vpc_id
  ecs_sg_id                  = module.ecs.ecs_sg_id
  private_subnet_ids         = module.vpc.private_subnets[*].id
  private_subnet_cidr_blocks = module.vpc.private_subnets[*].cidr_block
  db_name                    = var.db_name
  db_username                = var.db_username
  db_password                = var.db_password
  iam_user_name              = var.iam_user_name
}
