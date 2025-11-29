terraform {
  backend "s3" {
    bucket         = "kd-testing-pyramid-s3-bucket"
    key            = "testing-pyramid/terraform.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
