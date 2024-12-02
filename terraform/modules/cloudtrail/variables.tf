variable "region" {
  description = "AWS region"
  type        = string
}

variable "bucket_name" {
  description = "Name of the S3 bucket for audit logs"
  type        = string
}

variable "trail_name" {
  description = "Name of the CloudTrail trail"
  type        = string
}
