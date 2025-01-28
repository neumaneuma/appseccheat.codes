output "main_state_bucket_name" {
  value = aws_s3_bucket.main_state.id
}

output "main_dynamodb_table_name" {
  value = aws_dynamodb_table.main_locks.name
}

output "iam_state_bucket_name" {
  value = aws_s3_bucket.iam_state.id
}

output "iam_dynamodb_table_name" {
  value = aws_dynamodb_table.iam_locks.name
}
