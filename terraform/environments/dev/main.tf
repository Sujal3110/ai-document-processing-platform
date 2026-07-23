terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
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

module "iam" {
  source = "../../modules/iam"

  project_name  = "ai-doc-processing"
  environment   = "dev"
  s3_bucket_arn = module.s3.bucket_arn
}

module "lambda" {
  source = "../../modules/lambda"

  project_name    = "ai-doc-processing"
  environment     = "dev"
  lambda_role_arn = module.iam.lambda_role_arn
  s3_bucket_arn   = module.s3.bucket_arn
}

# Permission for S3 to invoke Lambda (moved here for correct dependency ordering)
resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda.lambda_function_name
  principal     = "s3.amazonaws.com"
  source_arn    = module.s3.bucket_arn
}

# S3 notification — depends_on ensures permission exists first
resource "aws_s3_bucket_notification" "document_upload" {
  bucket = module.s3.bucket_name

  lambda_function {
    lambda_function_arn = module.lambda.lambda_function_arn
    events               = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_s3]
}