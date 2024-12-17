resource "aws_ecr_repository" "repo" {
  name                 = var.repo_name
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "AES256"
  }
}

resource "aws_security_group" "allow_tls" {
  name        = "allow_tls"
  description = "Allow TLS inbound traffic and all outbound traffic"
  vpc_id      = var.vpc_id

  tags = {
    Name = "allow_tls"
  }
}

resource "aws_vpc_security_group_ingress_rule" "alb_public_traffic" {
  description       = "Allow HTTPS public traffic to the ALB"
  count             = length(var.public_subnet_cidr_blocks)
  security_group_id = aws_security_group.allow_tls.id
  cidr_ipv4         = var.public_subnet_cidr_blocks[count.index]
  from_port         = 443
  ip_protocol       = "tcp"
  to_port           = 443
}

resource "aws_vpc_security_group_egress_rule" "alb_private_traffic" {
  description       = "Allow ALB to communicate with the ECS instances"
  count             = length(var.private_subnet_cidr_blocks)
  security_group_id = aws_security_group.allow_tls.id
  cidr_ipv4         = var.private_subnet_cidr_blocks[count.index]
  # from_port         = 443
  #ip_protocol       = "tcp"
  # to_port           = 12301
  ip_protocol = "-1" # semantically equivalent to all ports until i verify everything works
}

resource "aws_security_group" "ecs_sg" {
  name   = "ecs_sg"
  vpc_id = var.vpc_id

  tags = {
    Name = "ecs_sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_alb_to_ecs" {
  description                  = "Allow ECS instances to receive traffic from the ALB"
  security_group_id            = aws_security_group.ecs_sg.id
  referenced_security_group_id = aws_security_group.allow_tls.id
  from_port                    = 12301
  to_port                      = 12301
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "allow_ecs_to_alb" {
  description       = "Allow ECS instances to send traffic to the ALB"
  count             = length(var.private_subnet_cidr_blocks)
  security_group_id = aws_security_group.ecs_sg.id
  cidr_ipv4         = var.private_subnet_cidr_blocks[count.index]
  # from_port         = 443
  #ip_protocol       = "tcp"
  # to_port           = 12301
  ip_protocol = "-1" # semantically equivalent to all ports until i verify everything works
}

resource "aws_lb" "main" {
  name               = "app-load-balancer"
  internal           = false
  load_balancer_type = "application"
  subnets            = var.public_subnet_ids
  security_groups    = [aws_security_group.allow_tls.id]
}

resource "aws_lb_listener" "main" {
  load_balancer_arn = aws_lb.main.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.alb_certificate_arn

  # this can be broken out into a `aws_lb_listener_rule` resource if it needs to be more complex
  default_action {
    type = "forward"
    forward {
      target_group {
        arn    = aws_lb_target_group.blue.arn
        weight = lookup(local.traffic_dist_map[var.traffic_distribution], "blue", 100)
      }

      # target_group {
      #   arn    = aws_lb_target_group.green.arn
      #   weight = lookup(local.traffic_dist_map[var.traffic_distribution], "green", 0)
      # }

      stickiness {
        enabled  = false
        duration = 1
      }
    }
  }
}

resource "aws_lb_target_group" "blue" {
  name     = "blue-target-group"
  port     = 12301
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
}

resource "aws_s3_bucket" "ecs_logs" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_lifecycle_configuration" "logs_cleanup" {
  bucket = aws_s3_bucket.ecs_logs.id

  rule {
    id     = "cleanup"
    status = "Enabled"

    expiration {
      days = 7
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "ecs_logs" {
  bucket = aws_s3_bucket.ecs_logs.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "ecs_logs" {
  bucket = aws_s3_bucket.ecs_logs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_ecs_cluster" "main" {
  name = "main-cluster"

  setting {
    name  = "containerInsights"
    value = "disabled"
  }

  configuration {
    execute_command_configuration {
      logging = "OVERRIDE"
      log_configuration {
        s3_bucket_name = aws_s3_bucket.ecs_logs.id
      }
    }
  }
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "ecs_role" {
  name               = "ecs-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_instance_profile" "ecs_instance_profile" {
  name = "ecs-instance-profile"
  role = aws_iam_role.ecs_role.name
}

# https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html
# Can manually examine this via `aws ssm get-parameter --name "/aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id" --region us-east-1`
data "aws_ssm_parameter" "ecs_optimized_ami" {
  name = "/aws/service/ecs/optimized-ami/amazon-linux-2023/recommended/image_id"
}

resource "aws_launch_template" "ecs" {
  name_prefix   = "ecs-template"
  image_id      = data.aws_ssm_parameter.ecs_optimized_ami.value
  instance_type = "t2.micro"

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "ecs-instance"
    }
  }

  # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/launch_container_instance.html
  # Fargate abstracts away this hackiness; EC2 instances require this.
  user_data = base64encode(<<-EOF
              #!/bin/bash
              echo ECS_CLUSTER=${aws_ecs_cluster.main.name} >> /etc/ecs/ecs.config
              EOF
  )

  iam_instance_profile {
    name = aws_iam_instance_profile.ecs_instance_profile.name
  }
}

resource "aws_autoscaling_group" "ecs" {
  name_prefix         = "ecs-asg"
  desired_capacity    = 1
  max_size            = 1
  min_size            = 1
  vpc_zone_identifier = var.private_subnet_ids

  launch_template {
    id      = aws_launch_template.ecs.id
    version = "$Latest"
  }
}

resource "aws_autoscaling_attachment" "backend" {
  autoscaling_group_name = aws_autoscaling_group.ecs.id
  lb_target_group_arn    = aws_lb_target_group.blue.arn
}


resource "aws_ecs_task_definition" "backend" {
  family                   = "backend"
  network_mode             = "bridge"
  requires_compatibilities = ["EC2"]
  cpu                      = "768"
  memory                   = "768"

  container_definitions = jsonencode([
    {
      name      = "backend"
      command   = ["fastapi", "--host", "0.0.0.0", "--port", "12301", "main.py"]
      image     = "${aws_ecr_repository.repo.repository_url}:backend"
      essential = true
      portMappings = [
        {
          containerPort = 12301
          hostPort      = 12301
        }
      ]
    }
  ])
}

resource "aws_ecs_task_definition" "internal_api" {
  family                   = "internal-api"
  network_mode             = "bridge"
  requires_compatibilities = ["EC2"]
  cpu                      = "256"
  memory                   = "196"

  container_definitions = jsonencode([
    {
      name      = "internal-api"
      command   = ["fastapi", "--host", "0.0.0.0", "--port", "12302", "main.py"]
      image     = "${aws_ecr_repository.repo.repository_url}:internal_api"
      essential = true
      portMappings = [
        {
          containerPort = 12302
          hostPort      = 12302
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "backend" {
  name            = "backend"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.backend.arn
  desired_count   = 1

  load_balancer {
    target_group_arn = aws_lb_target_group.blue.arn
    container_name   = "backend"
    container_port   = 12301
  }

  depends_on = [
    aws_lb_listener.main
  ]
}

resource "aws_ecs_service" "internal_api" {
  name            = "internal-api"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.internal_api.arn
  desired_count   = 1
}
