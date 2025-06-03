output "frontend_public_ip" {
  description = "Public IP of the frontend instance"
  value       = aws_instance.frontend.public_ip
}

output "backend_public_ip" {
  description = "Public IP of the backend instance"
  value       = aws_instance.backend.public_ip
}
