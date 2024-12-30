output "db_host" {
  value = aws_db_instance.postgres_db.address
}

output "db_security_group_id" {
  value = aws_security_group.database.id
}
