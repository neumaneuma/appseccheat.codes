terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

resource "aws_security_group" "database" {
  name        = "db-sg"
  description = "Security group for database"
  vpc_id      = var.vpc_id
}

resource "aws_vpc_security_group_ingress_rule" "database_sg_ipv4" {
  security_group_id            = aws_security_group.database.id
  from_port                    = 5432
  ip_protocol                  = "tcp"
  to_port                      = 5432
  referenced_security_group_id = var.ecs_sg_id
}

resource "aws_db_subnet_group" "database" {
  name       = "db-private-subnets-group"
  subnet_ids = var.private_subnet_ids
}

resource "aws_db_instance" "postgres_db" {
  identifier                 = "postgres-db"
  engine                     = "postgres"
  engine_version             = "17.1"
  instance_class             = "db.t4g.micro"
  allocated_storage          = 20
  max_allocated_storage      = 0 # Disable auto-scaling
  auto_minor_version_upgrade = false
  skip_final_snapshot        = true # don't create a snapshot when the db is deleted

  db_subnet_group_name   = aws_db_subnet_group.database.name
  vpc_security_group_ids = [aws_security_group.database.id]

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  port     = 5432

  backup_retention_period  = 3
  delete_automated_backups = true

  storage_encrypted   = true # no need to have a KMS key with this argument
  storage_type        = "gp2"
  network_type        = "IPV4"
  publicly_accessible = false

  performance_insights_enabled          = true
  performance_insights_retention_period = 7
}
