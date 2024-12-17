variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "domain_name" {
  description = "Domain name"
  type        = string
  default     = "appseccheat.codes"
}

variable "cloudflare_api_token" {
  description = "Cloudflare API token"
  type        = string
  default     = null # force terraform to use $CLOUDFLARE_API_TOKEN environment variable
  sensitive   = true
}

variable "traffic_distribution" {
  description = "Levels of traffic distribution"
  type        = string
  default     = "blue"
}

variable "ecr_repo_name" {
  description = "ECR repository name"
  type        = string
  default     = "appseccheat.codes"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "postgres"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "iam_user_name" {
  description = "IAM user name"
  type        = string
  default     = "iam_user" # hardcoded to match the terraform/iam/main.tf file
}
