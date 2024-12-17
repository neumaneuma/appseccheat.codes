output "cloudfront_distribution_domain" {
  value = module.cdn.cloudfront_distribution_domain_name
}

output "cdn_s3_bucket_name" {
  value = module.cdn.s3_bucket_name
}

output "cloudtrail_s3_bucket_name" {
  value = module.cloudtrail.s3_bucket_name
}

output "ecs_logs_s3_bucket_name" {
  value = module.ecs.s3_bucket_name
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "ecr_repository_url" {
  value = module.ecs.repo_url
}

output "ecr_repository_name" {
  value = var.ecr_repo_name
}

output "db_host" {
  value = module.database.db_host
}
