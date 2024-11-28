# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

provider "aws" {
  region = var.region
}

data "aws_availability_zones" "available" {}

# this module abstracts away the details of creating a VPC through tf resources. what it's composed of:
# - VPC (like a datacenter)
# - public subnets
# - internet gateway (like a router/modem combo)
# - route tables (how the public subnet talks to the internet gateway)
# - private subnets (where the db will live, all subnets on the same vpc can talk to each other by default, whether they are public or private)

# Internet
#     ↕
# [Internet Gateway]                  # Internet access point
#     ↕
# [Route Table (Public)]             # Routes: 0.0.0.0/0 → IGW
#     ↕
# Public Subnet                      # CIDR: 10.0.1.0/24
# ├── Load Balancer                  # Public IP: 54.239.31.200
# ├── EC2 instances                  # Public IP
#     ↕
# Private Subnet                     # CIDR: 10.0.2.0/24
# └── RDS database                   # Private IP: 10.0.2.20

# # 1. Internet Gateway
# resource "aws_internet_gateway" "main" {
#   vpc_id = aws_vpc.main.id
# }

# # 2. Public Route Table
# resource "aws_route_table" "public" {
#   vpc_id = aws_vpc.main.id
# }

# resource "aws_route" "public_internet" {
#   route_table_id         = aws_route_table.public.id
#   destination_cidr_block = "0.0.0.0/0"
#   gateway_id             = aws_internet_gateway.main.id
# }

# # 3. Public Subnet
# resource "aws_subnet" "public" {
#   vpc_id     = aws_vpc.main.id
#   cidr_block = "10.0.1.0/24"
# }

# resource "aws_route_table_association" "public" {
#   subnet_id      = aws_subnet.public.id
#   route_table_id = aws_route_table.public.id
# }

# # 4. Private Route Table
# resource "aws_route_table" "private" {
#   vpc_id = aws_vpc.main.id
# }

# resource "aws_route" "private_internet" {
#   route_table_id         = aws_route_table.private.id
#   destination_cidr_block = "0.0.0.0/0"
#   nat_gateway_id         = aws_nat_gateway.main.id
# }

# # 5. Private Subnet
# resource "aws_subnet" "private" {
#   vpc_id     = aws_vpc.main.id
#   cidr_block = "10.0.2.0/24"
# }

# resource "aws_route_table_association" "private" {
#   subnet_id      = aws_subnet.private.id
#   route_table_id = aws_route_table.private.id
# }

# # 6. Security Groups
# resource "aws_security_group" "lb" {
#   name   = "lb"
#   vpc_id = aws_vpc.main.id

#   ingress {
#     from_port   = 80
#     to_port     = 80
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# }

# resource "aws_security_group" "ec2" {
#   name   = "ec2"
#   vpc_id = aws_vpc.main.id

#   ingress {
#     from_port       = 80
#     to_port         = 80
#     protocol        = "tcp"
#     security_groups = [aws_security_group.lb.id]
#   }
# }

# resource "aws_security_group" "rds" {
#   name   = "rds"
#   vpc_id = aws_vpc.main.id

#   ingress {
#     from_port       = 5432
#     to_port         = 5432
#     protocol        = "tcp"
#     security_groups = [aws_security_group.ec2.id]
#   }
# }
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "2.77.0"

  name                 = "education"
  cidr                 = "10.0.0.0/16"
  azs                  = data.aws_availability_zones.available.names
  public_subnets       = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
  enable_dns_hostnames = true
  enable_dns_support   = true
}

# a subnet is just a contiguous range of IP addresses.
# a db subnet group contains at least 2 subnets in different AZs. aws will automatically assign the db instance an ip address from the subnet.
resource "aws_db_subnet_group" "education" {
  name       = "education"
  subnet_ids = module.vpc.public_subnets

  tags = {
    Name = "Education"
  }
}

# basically a virtual firewall that controls the traffic for the db.
resource "aws_security_group" "rds" {
  name   = "education_rds"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "education_rds"
  }
}

# represents db-engine-specific parameters.
resource "aws_db_parameter_group" "education" {
  name   = "education"
  family = "postgres17"

  parameter {
    name  = "log_connections"
    value = "1"
  }
}

# represents a db instance. core settings config set here
resource "aws_db_instance" "education" {
  identifier              = "education"
  instance_class          = "db.t3.micro"
  allocated_storage       = 10
  engine                  = "postgres"
  engine_version          = "17.1"
  username                = "edu"
  password                = var.db_password
  db_subnet_group_name    = aws_db_subnet_group.education.name
  vpc_security_group_ids  = [aws_security_group.rds.id]
  parameter_group_name    = aws_db_parameter_group.education.name
  publicly_accessible     = true
  skip_final_snapshot     = true
  apply_immediately       = true
  backup_retention_period = 1
}

resource "aws_db_instance" "education_replica" {
  identifier             = "education-replica"
  replicate_source_db    = aws_db_instance.education.identifier
  instance_class         = "db.t3.micro"
  apply_immediately      = true
  publicly_accessible    = true
  skip_final_snapshot    = true
  vpc_security_group_ids = [aws_security_group.rds.id]
  parameter_group_name   = aws_db_parameter_group.education.name
}
