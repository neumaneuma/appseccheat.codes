import sys

import boto3

bucket_name = sys.argv[1]
s3 = boto3.resource("s3")
bucket = s3.Bucket(bucket_name)
bucket.object_versions.delete()
print(f"Deleted all versions of {bucket_name}")
