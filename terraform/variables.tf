variable "aws_region" {
  description = "AWS region"
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name"
  default     = "production"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  default     = "10.0.0.0/16"
}

variable "domain_name" {
  description = "Domain name for the application"
  type        = string
}

variable "frontend_bucket_name" {
  description = "Name of the S3 bucket for frontend"
  type        = string
}

variable "backend_image" {
  description = "Docker image for backend service"
  type        = string
}

variable "internal_api_image" {
  description = "Docker image for internal API service"
  type        = string
}

variable "db_name" {
  description = "Database name"
  default     = "postgres"
}

variable "db_username" {
  description = "Database username"
  type        = string
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
