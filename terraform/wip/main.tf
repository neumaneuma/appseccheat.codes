terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC and Networking
# module "vpc" {
#   source = "./modules/vpc"

#   environment = var.environment
#   vpc_cidr    = var.vpc_cidr
# }

# # Frontend
# module "frontend" {
#   source = "./modules/frontend"

#   environment         = var.environment
#   domain_name        = var.domain_name
#   frontend_bucket    = var.frontend_bucket_name
# }

# # Backend Services
# module "backend" {
#   source = "./modules/backend"

#   environment     = var.environment
#   vpc_id         = module.vpc.vpc_id
#   private_subnets = module.vpc.private_subnets

#   backend_image      = var.backend_image
#   internal_api_image = var.internal_api_image

#   db_host     = module.database.db_host
#   db_name     = var.db_name
#   db_username = var.db_username
#   db_password = var.db_password
# }

# Database
module "database" {
  source = "./modules/database"

  environment     = var.environment
  vpc_id          = module.vpc.vpc_id
  private_subnets = module.vpc.private_subnets

  db_name     = var.db_name
  db_username = var.db_username
  db_password = var.db_password
}
