resource "aws_db_instance" "postgres" {
  identifier        = "production-db"
  engine            = "postgres"
  engine_version    = "15.1"
  instance_class    = "db.t4g.micro"
  allocated_storage = 2

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.database.id]
  db_subnet_group_name   = aws_db_subnet_group.database.name

  skip_final_snapshot = true

  tags = {
    Environment = "production"
  }
}

resource "aws_security_group" "database" {
  name        = "production-database-sg"
  description = "Security group for database"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = []  # Will need to be updated with application security group
  }
}

resource "aws_db_subnet_group" "database" {
  name       = "production-database-subnet-group"
  subnet_ids = var.private_subnets

  tags = {
    Environment = "production"
  }
}

output "db_host" {
  value = aws_db_instance.postgres.endpoint
}
