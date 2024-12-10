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
