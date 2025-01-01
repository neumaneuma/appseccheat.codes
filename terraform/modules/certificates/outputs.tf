output "alb_certificate_arn" {
  value       = aws_acm_certificate.alb.arn
  description = "ARN of ALB certificate"
}

output "origin_certificate" {
  value       = cloudflare_origin_ca_certificate.cert.certificate
  description = "Cloudflare Origin Certificate"
  sensitive   = true
}

output "private_key_pem" {
  value       = tls_private_key.private_key.private_key_pem
  description = "Private key for Cloudflare Origin Certificate"
  sensitive   = true
}
