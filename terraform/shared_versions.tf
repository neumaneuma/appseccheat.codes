terraform {
  # https://developer.hashicorp.com/terraform/language/expressions/version-constraints
  # use version = ">= a.b.c" when want to upgrade, manually copy the latest version here (pretty mid, maybe
  # can write a script to do this), then run terraform init -upgrade
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.84.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "5.0.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.6.3"
    }
    http = {
      source  = "hashicorp/http"
      version = "3.4.5"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "4.0.6"
    }
  }
  required_version = "~> 1.5"
}
