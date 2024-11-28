resource "aws_db_instance" "postgres_db" {
  identifier                 = "${var.environment}-db"
  engine                     = "postgres"
  engine_version             = "17.1"
  instance_class             = "db.t4g.micro"
  allocated_storage          = 20
  max_allocated_storage      = 0 # Disable auto-scaling
  auto_minor_version_upgrade = false
  skip_final_snapshot        = true # don't create a snapshot when the db is deleted

  username = var.db_username
  password = var.db_password
  port     = 5432

  backup_retention_period  = 3
  delete_automated_backups = true

  kms_key_id          = data.aws_kms_key.db_encryption_key.arn
  storage_encrypted   = true
  storage_type        = "gp2"
  network_type        = "IPV4"
  publicly_accessible = false

  performance_insights_enabled          = true
  performance_insights_retention_period = 7
  performance_insights_kms_key_id       = aws_kms_key.db_encryption_key.arn
}
