terraform {
  backend "s3" {
    bucket         = "kd-endgame-assignment-s3-bucket"
    key            = "endgame-assignment/terraform.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "kd-terraform-state-lock"
    encrypt        = true
  }
}
