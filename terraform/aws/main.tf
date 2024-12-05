terraform {
  backend "s3" {
    bucket         = "terraform-state-ab09aedc-2127-60e3-d7e2-544c0cab76d4"
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
