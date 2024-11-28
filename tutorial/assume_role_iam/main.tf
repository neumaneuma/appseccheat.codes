# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

provider "aws" {
  alias                    = "source"
  region                   = "us-east-1"
  profile                  = "source"
}

provider "aws" {
  alias                    = "destination"
  region                   = "us-east-1"
  profile                  = "destination"
}

data "aws_caller_identity" "source" {
  provider = aws.source
}

# this is an aws managed policy
data "aws_iam_policy" "ec2" {
  provider = aws.destination
  name     = "AmazonEC2FullAccess"
}

data "aws_iam_policy_document" "assume_role" {
  provider = aws.destination
  statement {
    actions = [
      "sts:AssumeRole",
      "sts:TagSession",
      "sts:SetSourceIdentity"
    ]
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.source.account_id}:root"] # allows all users of the source account to use any role with the policy attached.
    }
  }
}

resource "aws_iam_role" "assume_role" {
  provider            = aws.destination
  name                = "assume_role"
  assume_role_policy  = data.aws_iam_policy_document.assume_role.json
  tags                = {}
}

resource "aws_iam_role_policy_attachment" "assume_role_policy_attachment" {
  role       = aws_iam_role.assume_role.name
  policy_arn = data.aws_iam_policy.ec2.arn
}
