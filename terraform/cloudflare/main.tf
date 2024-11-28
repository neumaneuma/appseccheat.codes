terraform {
  backend "s3" {
    bucket         = "terraform-state-64ec6d21-b96a-b7bc-7cd2-d3d4284d5ffc"
    key            = "state/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-locks"
  }
}

provider "cloudflare" {}

data "cloudflare_zones" "domain" {
  filter {
    name = var.domain
  }
}

# https://registry.terraform.io/providers/cloudflare/cloudflare/4.47.0/docs/resources/record
resource "cloudflare_record" "cname" {
  zone_id = data.cloudflare_zones.domain.zones[0].id
  name    = var.domain
  content = aws_s3_bucket_website_configuration.site.website_endpoint
  type    = "CNAME"
}
