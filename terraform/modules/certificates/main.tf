terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
    cloudflare = {
      source = "cloudflare/cloudflare"
    }
    tls = {
      source = "hashicorp/tls"
    }
  }
}

resource "tls_private_key" "private_key" {
  algorithm   = "ECDSA"
  ecdsa_curve = "P256"
}

resource "tls_cert_request" "csr" {
  private_key_pem = tls_private_key.private_key.private_key_pem

  subject {
    common_name  = var.api_domain_name
    organization = "AppSec Cheat Codes"
  }
}

resource "cloudflare_origin_ca_certificate" "cert" {
  csr                = tls_cert_request.csr.cert_request_pem
  hostnames          = [var.api_domain_name]
  request_type       = "origin-ecc"
  requested_validity = 365
}
