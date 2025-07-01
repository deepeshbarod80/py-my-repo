terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket"
    key            = "vpn/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}