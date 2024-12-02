terraform {
  backend "s3" {
    bucket         = "terraform-state-64ec6d21-b96a-b7bc-7cd2-d3d4284d5ffc"
    key            = "state/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-locks"
  }
}

provider "aws" {
  alias  = "us-east-1"
  region = "us-east-1"
}

provider "cloudflare" {}

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
}

module "cdn" {
  source                     = "../modules/cdn"
  region                     = var.region
  domain_name                = var.domain_name
  origin_id                  = "S3Origin"
  bucket_name                = "cloudfront-cdn-bucket-${random_uuid.uuid.result}"
  cloudfront_certificate_arn = module.certificates.cloudfront_certificate_arn
}
