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




resource "aws_iam_user" "deployer" {
  name = "deployer"
}

resource "aws_iam_access_key" "deployer" {
  user = aws_iam_user.deployer.name
}

data "aws_iam_policy_document" "deployer" {
  statement {
    effect = "Allow"
    actions = [
      # "ec2:CreateVpc",
      # "ec2:DeleteVpc",
      # "ec2:ModifyVpcAttribute",
      "ec2:DescribeVpcs",

      # Subnets
      # "ec2:CreateSubnet",
      # "ec2:DeleteSubnet",
      # "ec2:ModifySubnetAttribute",
      "ec2:DescribeSubnets",

      # Internet Gateway
      # "ec2:CreateInternetGateway",
      # "ec2:DeleteInternetGateway",
      # "ec2:AttachInternetGateway",
      # "ec2:DetachInternetGateway",
      "ec2:DescribeInternetGateways",

      # Route Tables
      # "ec2:CreateRouteTable",
      # "ec2:DeleteRouteTable",
      # "ec2:CreateRoute",
      # "ec2:DeleteRoute",
      # "ec2:AssociateRouteTable",
      # "ec2:DisassociateRouteTable",
      # "ec2:ReplaceRoute",
      "ec2:DescribeRouteTables",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "deployer" {
  policy = data.aws_iam_policy_document.deployer.json
}

resource "aws_iam_user_policy_attachment" "deployer-attach" {
  user       = aws_iam_user.deployer.name
  policy_arn = aws_iam_policy.deployer.arn
}
