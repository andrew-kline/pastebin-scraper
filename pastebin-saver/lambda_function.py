import json
import logging
import os

import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.client('dynamodb')
table_name = os.environ.get("DYNAMODB_TABLE")
s3_resource = boto3.resource("s3", region_name="us-east-1")
bucket_name = os.environ.get("S3_BUCKET")

def lambda_handler(event, context):
    response = dynamodb.scan(
        TableName=table_name,
        FilterExpression="attribute_not_exists(s3_url)"
    )

    saved_pastes = []
    for item in response.get("Items"):
        paste_key = item.get("paste_key", {}).get("S")
        scrape_url = item.get("scrape_url", {}).get("S")
        logger.info(f"Retrieving {paste_key} from {scrape_url}")
        resp = requests.get(scrape_url)
        if resp.status_code != 200:
            logger.error(f"Error while saving scrape {paste_key} - {resp.status_code}")
            continue
        
        s3_resource.Object(bucket_name, f"{paste_key}.txt").put(Body=resp.text)
        s3_url = f"s3://{bucket_name}/{paste_key}.txt"
        dynamodb.update_item(
            TableName=table_name,
            Key={"paste_key": paste_key},
            UpdateExpression="Set #field = :value",
            ExpressionAttributeNames={
                "#field": "s3_url"
            },
            ExpressionAttributeValues={
                ":value": s3_url
            },
            ReturnValues="UPDATED_NEW"
        )
        saved_pastes.append(paste_key)
        logger.info(f"Saved {paste_key} to {s3_url}")

    return {
        "success": True,
        "saved_pastes": saved_pastes
    }