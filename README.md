# pastebin-scraper

Key order of operations:
1. Deploy pastebin_ddb and pastebin_s3 first. These will not be deleted if the stacks are deleted, and should be managed somewhat separately. They shouldn't be touched often, if at all
2. Deploy the lambdas via deploy.sh. Key flags are --profile (AWS profile name), --region (AWS region), and --codebucket (S3 bucket where the lambda code should live) 