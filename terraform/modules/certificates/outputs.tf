output "cloudfront_certificate_arn" {
  value       = aws_acm_certificate.cloudfront.arn
  description = "ARN of CloudFront certificate"
}

output "alb_certificate_arn" {
  value       = aws_acm_certificate.alb.arn
  description = "ARN of ALB certificate"
}
