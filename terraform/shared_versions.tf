terraform {
  # use >= when want to upgrade
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.83.1"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "4.50.0"
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
