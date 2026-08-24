# Illustrative infrastructure-as-code snippet for the written report.
# NOT applied to any real account: it demonstrates how the production
# host would be defined as reviewable, versioned code instead of a
# hand-configured server, and how cost-attribution tags are enforced.

terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

variable "region" {
  description = "AWS region the service runs in"
  type        = string
  default     = "eu-west-1"
}

variable "environment" {
  description = "Deployment environment (staging or production)"
  type        = string
  default     = "staging"
}

resource "aws_instance" "app" {
  # Placeholder AMI: in real use this is resolved with an aws_ami data
  # source pinned to a hardened base image.
  ami           = "ami-00000000000000000"
  instance_type = "t3.small"

  tags = {
    Name        = "nimbus-notes-${var.environment}"
    Environment = var.environment
    Owner       = "platform-team"
    CostCentre  = "engineering"
    ManagedBy   = "terraform"
  }
}

output "app_instance_id" {
  description = "Instance id, consumed by deploy tooling"
  value       = aws_instance.app.id
}
