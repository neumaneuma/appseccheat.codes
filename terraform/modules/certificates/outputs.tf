output "alb_certificate_arn" {
  value       = aws_acm_certificate.alb.arn
  description = "ARN of ALB certificate"
}
