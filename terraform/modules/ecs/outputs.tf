output "s3_bucket_name" {
  value = aws_s3_bucket.ecs_logs.id
}

output "ecs_sg_id" {
  value = aws_security_group.ecs_sg.id
}
output "asg_name" {
  value = aws_autoscaling_group.ecs.name
}

output "ecs_service_name" {
  value = aws_ecs_service.multi_container_service.name
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "ec2_eip_address" {
  description = "EIP address of the ECS EC2 instance"
  value       = aws_eip.ec2_host_eip.public_ip
}
