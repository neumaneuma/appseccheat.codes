# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.example.id
}

output "asg_id" {
  description = "Auto Scaling group ID"
  value       = aws_autoscaling_group.example.id
}
