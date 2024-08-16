codebucket_default="awkwarden-pastebin-scraper-cf"
profile_default="akawk"
region_default="us-east-1"

# Parse command line arguments
while [ $# -gt 0 ]; do
  case "$1" in
    --codebucket=*)
      codebucket="${1#*=}"
      ;;
    --profile=*)
      profile="${1#*=}"
      ;;
    --region=*)
      region="${1#*=}"
      ;;
    *)
      echo "Invalid argument: $1"
      exit 1
  esac
  shift
done

# Assign default values if not provided
codebucket="${codebucket:-$codebucket_default}"
profile="${profile:-$profile_default}"
region="${region:-$region_default}"


mkdir -p old
mv *.zip old/
cd pastebin-saver
pip install --target requirements -r requirements.txt
cd requirements/
zip -r ../../pastebin-saver.zip .
cd ..
chmod 755 lambda_function.py
zip ../pastebin-saver.zip lambda_function.py
cd ..
cd pastebin-scraper
pip install --target requirements -r requirements.txt
cd requirements/
zip -r ../../pastebin-scraper.zip .
cd ..
chmod 755 lambda_function.py
zip ../pastebin-scraper.zip lambda_function.py
cd ..
scraper_hash=$(openssl sha256  pastebin-scraper.zip | cut -f 2 -d " ")
mv pastebin-scraper.zip pastebin-scraper-$scraper_hash.zip
saver_hash=$(openssl sha256  pastebin-saver.zip | cut -f 2 -d " ")
mv pastebin-saver.zip pastebin-saver-$saver_hash.zip
rm -rf old/
aws s3 cp pastebin-scraper-$scraper_hash.zip s3://$codebucket/code/ --profile $profile
aws s3 cp pastebin-saver-$saver_hash.zip s3://$codebucket/code/ --profile $profile
command="aws cloudformation deploy --tags project=pastebin-scraper --profile $profile --region $region --capabilities CAPABILITY_IAM --parameter-overrides PasteS3StackName=PasteSaveS3BucketStack PasteDDBStackName=PasteTrackingDynamoDBStack ScraperZipFileName=pastebin-scraper-$scraper_hash.zip SaverZipFileName=pastebin-saver-$saver_hash.zip CodeBucket=$codebucket --stack-name PasteCollectionLambdas --template ./pastebin_lambda.yaml"
echo $command
$command
