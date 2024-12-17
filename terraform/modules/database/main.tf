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
  referenced_security_group_id = var.alb_sg_id
}

resource "aws_db_subnet_group" "database" {
  name       = "db-private-subnets-group"
  subnet_ids = var.private_subnet_ids
}

resource "aws_kms_key" "db_encryption_key" {
  description              = "KMS key for database encryption"
  key_usage                = "ENCRYPT_DECRYPT"
  customer_master_key_spec = "SYMMETRIC_DEFAULT"
  is_enabled               = true
  deletion_window_in_days  = 14
  enable_key_rotation      = true
  rotation_period_in_days  = 180
  multi_region             = false
  policy                   = data.aws_iam_policy_document.kms_key_policy.json
}

data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "kms_key_policy" {
  source_policy_documents = []
  version                 = "2012-10-17"
  policy_id               = "key-default-1"

  statement {
    sid    = "Enable Root Account Permissions"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
    }
    actions   = ["kms:*"]
    resources = ["*"]
  }

  statement {
    sid    = "Enable IAM User/Role Permissions"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/${var.iam_user_name}"]
    }
    actions = [
      "kms:Create*",
      "kms:Describe*",
      "kms:Enable*",
      "kms:List*",
      "kms:Put*",
      "kms:Update*",
      "kms:Revoke*",
      "kms:Disable*",
      "kms:Get*",
      "kms:Delete*",
      "kms:TagResource",
      "kms:UntagResource",
      "kms:ScheduleKeyDeletion",
      "kms:CancelKeyDeletion",
      "kms:Encrypt",
      "kms:Decrypt",
      "kms:ReEncrypt*",
      "kms:GenerateDataKey*"
    ]
    resources = ["*"]
  }

  statement {
    sid    = "Allow RDS to use the key"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["rds.amazonaws.com"]
    }
    actions = [
      "kms:Decrypt",
      "kms:GenerateDataKey",
      "kms:CreateGrant",
      "kms:ReEncrypt*",
      "kms:DescribeKey"
    ]
    resources = ["*"]
  }
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

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  port     = 5432

  backup_retention_period  = 3
  delete_automated_backups = true

  kms_key_id          = aws_kms_key.db_encryption_key.arn
  storage_encrypted   = true
  storage_type        = "gp2"
  network_type        = "IPV4"
  publicly_accessible = false

  performance_insights_enabled          = true
  performance_insights_retention_period = 7
  performance_insights_kms_key_id       = aws_kms_key.db_encryption_key.arn
}
