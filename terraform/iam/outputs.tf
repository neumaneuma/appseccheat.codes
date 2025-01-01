output "deployer_access_key_id" {
  value = aws_iam_access_key.deployer.id
}

output "deployer_secret_key" {
  value     = aws_iam_access_key.deployer.secret
  sensitive = true
}
