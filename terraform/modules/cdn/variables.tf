variable "region" {
  description = "AWS region"
  type        = string
}

variable "domain_name" {
  description = "Domain name"
  type        = string
}

variable "bucket_name" {
  description = "S3 bucket name for the frontend"
  type        = string
}

variable "cloudfront_certificate_arn" {
  type        = string
  description = "ARN of the CloudFront certificate"
}

variable "origin_id" {
  description = "Origin ID"
  type        = string
}
