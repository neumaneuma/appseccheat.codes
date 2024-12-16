variable "region" {
  description = "AWS region"
  type        = string
}

variable "repo_name" {
  description = "ECR repository name"
  type        = string
}

variable "bucket_name" {
  description = "S3 bucket name for ECS logs"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "public_subnet_ids" {
  description = "Public subnet IDs"
  type        = list(string)
}

variable "private_subnet_ids" {
  description = "Private subnet IDs"
  type        = list(string)
}

variable "public_subnet_cidr_blocks" {
  description = "Public subnet CIDR blocks"
  type        = list(string)
}

variable "private_subnet_cidr_blocks" {
  description = "Private subnet CIDR blocks"
  type        = list(string)
}

locals {
  traffic_dist_map = {
    blue = {
      blue  = 100
      green = 0
    }
    blue-90 = {
      blue  = 90
      green = 10
    }
    split = {
      blue  = 50
      green = 50
    }
    green-90 = {
      blue  = 10
      green = 90
    }
    green = {
      blue  = 0
      green = 100
    }
  }
}

variable "traffic_distribution" {
  description = "Levels of traffic distribution"
  type        = string
}

variable "alb_certificate_arn" {
  description = "ALB certificate ARN"
  type        = string
}
