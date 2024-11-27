# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      Environment     = "Test"
      Service         = "Example"
      HashiCorp-Learn = "aws-default-tags"
    }
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"]
}

resource "aws_instance" "example" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"

  # overrides default tags
  tags = {
    Service   = "Custom"
    ManagedBy = "Resource"
  }
}


resource "aws_launch_template" "example" {
  name_prefix   = "learn-terraform-aws-default-tags-"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
}

# An Auto Scaling group is a collection of EC2 instances that use the same configuration. You can define the range of instances in an Auto Scaling group and the desired count, and the service will ensure that that number of instances is running at any given time. If an instance is terminated, the Auto Scaling group will launch another in its place using the launch configuration at the time.

# AWS Auto Scaling Groups (ASGs) dynamically create and destroy EC2 instances as defined in the ASG's configuration. Because these EC2 instances are created and destroyed by AWS, Terraform does not manage them, and is not directly aware of them. As a result, the AWS provider cannot apply your default tags to the EC2 instances managed by your ASG. You can, however, use a data source and dynamic blocks to apply the default tags set on the provider to EC2 instances managed by your ASG.
resource "aws_autoscaling_group" "example" {
  availability_zones = data.aws_availability_zones.available.names
  desired_capacity   = 1
  max_size           = 1
  min_size           = 1

  launch_template {
    id      = aws_launch_template.example.id
    version = "$Latest"
  }

  dynamic "tag" {
    for_each = data.aws_default_tags.current.tags
    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }
}

data "aws_default_tags" "current" {}
