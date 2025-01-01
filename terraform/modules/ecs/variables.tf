variable "region" {
  description = "AWS region"
  type        = string
}

variable "rds_instance_url" {
  description = "RDS instance URL"
  type        = string
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "docker_hub_repo" {
  description = "Docker Hub repository identifier"
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

variable "backend_cloudwatch_log_group_name" {
  description = "Cloudwatch log group name for backend"
  type        = string
}

variable "internal_api_cloudwatch_log_group_name" {
  description = "Cloudwatch log group name for internal_api"
  type        = string
}

variable "ec2_host_name" {
  description = "EC2 host name"
  type        = string
}

variable "db_security_group_id" {
  description = "Database security group ID"
  type        = string
}

variable "cloudflare_ipv4_addresses" {
  description = "Cloudflare IPv4 addresses"
  type        = list(string)
}

variable "origin_certificate" {
  description = "Cloudflare Origin Certificate"
  type        = string
  sensitive   = true
}

variable "private_key_pem" {
  description = "Private key for Cloudflare Origin Certificate"
  type        = string
  sensitive   = true
}
