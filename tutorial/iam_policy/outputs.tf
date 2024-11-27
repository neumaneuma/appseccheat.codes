# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

output "rendered_policy" {
  value = data.aws_iam_policy_document.example.json
}
