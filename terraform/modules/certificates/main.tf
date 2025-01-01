resource "aws_acm_certificate" "alb" {
  domain_name       = var.api_domain_name
  validation_method = "DNS"
  key_algorithm     = "EC_prime256v1"

  tags = {
    Name = "alb-cert"
  }

  lifecycle {
    create_before_destroy = true
  }
}

data "cloudflare_zones" "domain" {
  filter {
    name = var.domain_name
  }
}

# The dns records and their respective validation resources don't need explicit `depends_on` because
# Terraform can infer the dependency from the reference to the certificate in the `for_each` block.
resource "cloudflare_record" "alb_validation" {
  for_each = {
    for dvo in aws_acm_certificate.alb.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  ttl             = 60
  name            = each.value.name
  content         = each.value.record
  type            = each.value.type
  zone_id         = data.cloudflare_zones.domain.zones[0].id
}

resource "aws_acm_certificate_validation" "alb" {
  certificate_arn         = aws_acm_certificate.alb.arn
  validation_record_fqdns = [for record in cloudflare_record.alb_validation : record.hostname]
}

resource "tls_private_key" "private_key" {
  algorithm   = "ECDSA"
  ecdsa_curve = "P256"
}

resource "tls_cert_request" "csr" {
  private_key_pem = tls_private_key.private_key.private_key_pem

  subject {
    common_name  = var.domain_name
    organization = "AppSec Cheat Codes"
  }
}

resource "cloudflare_origin_ca_certificate" "cert" {
  csr                = tls_cert_request.csr.cert_request_pem
  hostnames          = [var.domain_name]
  request_type       = "origin-ecc"
  requested_validity = 90 # TODO change to 365
}
