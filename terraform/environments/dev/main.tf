terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

module "s3" {
  source = "../../modules/s3"

  project_name = "ai-doc-processing"
  environment  = "dev"
}