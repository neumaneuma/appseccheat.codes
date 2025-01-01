terraform {
  backend "s3" {
    bucket         = "terraform-state-fd98f914-e3a3-e024-c533-fb339fbb5be3"
    key            = "state/cloudflare.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-locks"
  }
}

provider "cloudflare" {}


data "terraform_remote_state" "aws" {
  backend = "s3"
  config = {
    bucket = "terraform-state-fd98f914-e3a3-e024-c533-fb339fbb5be3"
    key    = "state/terraform.tfstate"
    region = var.region
  }
}


data "cloudflare_zones" "domain" {
  filter {
    name = var.domain_name
  }
}

resource "cloudflare_record" "backend" {
  zone_id = data.cloudflare_zones.domain.zones[0].id
  name    = var.api_domain_name
  content = data.terraform_remote_state.aws.outputs.ec2_public_dns
  type    = "CNAME"
  proxied = true
}
