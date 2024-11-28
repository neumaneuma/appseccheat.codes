terraform {
  backend "s3" {
    bucket         = "terraform-state-64ec6d21-b96a-b7bc-7cd2-d3d4284d5ffc"
    key            = "state/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-locks"
  }
}

provider "aws" {
  region = var.region
}


module "cloudtrail" {
  source = "../modules/cloudtrail"
  region = var.region
}
