variable "aws_region" {
  default = "ap-southeast-1"
}

variable "frontend_key_name" {
  type        = string
}

variable "backend_key_name" {
  type        = string
}

variable "frontend_instance_type" {
}

variable "backend_instance_type" {
}

variable "frontend_ami" {
}

variable "backend_ami" {
}
