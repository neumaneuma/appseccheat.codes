cd aws
terraform init -upgrade
cd ../cloudflare
terraform init -upgrade
cd ../iam
terraform init -upgrade
cd ../state
terraform init -upgrade
cd ..
