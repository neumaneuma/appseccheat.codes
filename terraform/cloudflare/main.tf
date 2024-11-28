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
