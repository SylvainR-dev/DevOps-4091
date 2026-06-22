terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_opensearch_domain" "openclassrooms-p8" {
  domain_name    = "openclassrooms-p5-edo"
  engine_version = "Elasticsearch_7.10"

  cluster_config {
    instance_type = "t3.small.search"
  }

  ebs_options {
    ebs_enabled = true
    volume_size = 10
  }

  access_policies = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { AWS = "arn:aws:iam::476646938402:root" }
        Action    = "es:*"
        Resource  = "arn:aws:es:us-east-1:476646938402:domain/openclassrooms-p5-edo/*"
      },
      {
        Effect    = "Allow"
        Principal = { AWS = "*" }
        Action    = "es:*"
        Resource  = "arn:aws:es:us-east-1:476646938402:domain/openclassrooms-p5-edo/*"
        Condition = {
          IpAddress = {
            "aws:SourceIp" = ["2a01:cb18:8622:f300:6a07:5446:8958:b3a1/128"]
          }
        }
      }
    ]
  })

  tags = {
    Domain = "OpenClassrooms_P5_EDO"
  }
}

output "elasticsearch" {
  description = "URL de la base de données ElasticSearch"
  value       = aws_opensearch_domain.openclassrooms-p8.endpoint
}

output "kibana" {
  description = "URL de connexion à l'instance Kibana"
  value       = aws_opensearch_domain.openclassrooms-p8.dashboard_endpoint
}