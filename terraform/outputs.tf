output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "app_security_group_id" {
  description = "ID of application security group"
  value       = aws_security_group.app.id
}

output "db_security_group_id" {
  description = "ID of database security group"
  value       = aws_security_group.db.id
}

output "app_instance_id" {
  description = "ID of the application EC2 instance"
  value       = aws_instance.app.id
}

output "app_public_ip" {
  description = "Public IP of the application server"
  value       = aws_eip.app.public_ip
}

output "app_private_ip" {
  description = "Private IP of the application server"
  value       = aws_instance.app.private_ip
}

output "connection_string" {
  description = "SSH connection string"
  value       = "ssh -i ${var.key_name}.pem ubuntu@${aws_eip.app.public_ip}"
}

output "application_url" {
  description = "Application URL"
  value       = "http://${aws_eip.app.public_ip}:8080"
}

output "api_url" {
  description = "Backend API URL"
  value       = "http://${aws_eip.app.public_ip}:5000"
}
