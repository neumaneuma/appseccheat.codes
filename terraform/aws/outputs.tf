output "cloudfront_distribution_domain" {
  value = module.cdn.cloudfront_distribution_domain_name
}

output "cdn_s3_bucket_name" {
  value = module.cdn.s3_bucket_name
}
