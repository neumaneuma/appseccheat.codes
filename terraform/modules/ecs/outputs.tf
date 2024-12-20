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
