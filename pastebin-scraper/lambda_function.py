import logging
import os

import boto3
import requests


logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.client('dynamodb')
pastebin_url = "https://scrape.pastebin.com/api_scraping.php?limit=100"
table_name = os.environ.get("DYNAMODB_TABLE")

def lambda_handler(event, context):
    resp = requests.get(pastebin_url)
    if resp.status_code != 200:
        logger.error(f"Pastebin paste list unsuccessful - {resp.status_code}.")
        return {
            "success": False,
            "status_code": resp.status_code,
            "pastes_added": 0
        }
    
    logger.info("Pastebin paste list successful.")
    i = 0
    for paste in resp.json():
        logger.debug(f"Paste {i}: {paste}")
        db_response = dynamodb.put_item(
            Item={
                'paste_key': {
                    'S': paste.get("key"),
                },
                'scrape_url': {
                    'S': paste.get("scrape_url"),
                },
                'full_url': {
                    'S': paste.get("full_url"),
                },
                'date': {
                    'S': paste.get("date"),
                },
                'size': {
                    'S': paste.get("size"),
                },
                'title': {
                    'S': paste.get("title"),
                },
                'syntax': {
                    'S': paste.get("syntax"),
                },
                'user': {
                    'S': paste.get("user"),
                },
                'hits': {
                    'S': paste.get("hits"),
                },
                's3_url': {
                    'S': ''
                }
            },
            ReturnConsumedCapacity='TOTAL',
            TableName=table_name,
        )
        i += db_response.get("ConsumedCapacity").get("CapacityUnits")
    logger.info(f"Paste list caching successful. {i} pastes cached.")
    
    return {
        "success": True,
        "status_code": 200,
        "pastes_added": i
    }

if __name__ == "__main__":
    lambda_handler({}, {})