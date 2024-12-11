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

# Additional provider configuration for us-east-1 (required for ACM certificates)
provider "aws" {
  alias  = "us-east-1"
  region = "us-east-1"
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

# S3 bucket names must be globally unique, so we use a random UUID to generate a unique name
resource "random_uuid" "uuid" {}

module "cloudtrail" {
  source      = "../modules/cloudtrail"
  region      = var.region
  trail_name  = "permissions-audit-trail"
  bucket_name = "cloudtrail-audit-logs-${random_uuid.uuid.result}"
}

module "certificates" {
  source      = "../modules/certificates"
  domain_name = var.domain_name
  region      = var.region
  providers = {
    aws           = aws
    aws.us-east-1 = aws.us-east-1
  }
}

module "cdn" {
  source                     = "../modules/cdn"
  region                     = var.region
  domain_name                = var.domain_name
  origin_id                  = "S3Origin"
  bucket_name                = "cloudfront-cdn-bucket-${random_uuid.uuid.result}"
  cloudfront_certificate_arn = module.certificates.cloudfront_certificate_arn
}

module "vpc" {
  source = "../modules/vpc"
  region = var.region
}

module "ecs" {
  source               = "../modules/ecs"
  region               = var.region
  public_subnet_ids    = [module.vpc.public_subnets[0].id, module.vpc.public_subnets[1].id]
  traffic_distribution = var.traffic_distribution
  repo_name            = var.ecr_repo_name
}
