output "s3_bucket_name" {
  value = aws_s3_bucket.ecs_logs.id
}

output "ecs_sg_id" {
  value = aws_security_group.ecs_sg.id
}

output "alb_dns_name" {
  value = aws_lb.main.dns_name
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

output "ec2_public_dns" {
  description = "Public DNS name of the ECS EC2 instance"
  value       = data.aws_instance.ecs_managed_ec2_host.public_dns
}
