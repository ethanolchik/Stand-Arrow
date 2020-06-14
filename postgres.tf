variable "allowed_ips" {
  type = list[string]
}

variable "postgres_password" {
  type = string
}

variable "postgres_username" {
  type = string
}

provider "aws" {
  profile = "default"
  shared_credentials_file = "$HOME/.aws/credentials"
  region  = "us-east-1"
}

resource "aws_security_group" "allow_postgres" {
  name        = "allow_postgres"
  description = "Allow Postgres Traffic"

  ingress {
    description = "TCP and My IP"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = var.allowed_ips
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "default" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "postgres"
  instance_class       = "db.t2.micro"
  name                 = "standarrow"
  username             = var.postgres_username
  password             = var.postgres_password
  publicly_accessible  = "true"
  vpc_security_group_ids = [aws_security_group.allow_postgres.id]
}
