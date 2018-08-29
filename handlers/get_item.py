'''Put item'''

import json
import logging
import os

import boto3
from tenacity import retry, stop_after_delay, wait_random_exponential

log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.root.setLevel(logging.getLevelName(log_level))  # type: ignore
_logger = logging.getLogger(__name__)

# DynamoDB
DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
DDB_TABLE_HASH_KEY = os.environ.get('DDB_TABLE_HASH_KEY')
dynamodb = boto3.resource('dynamodb')
DDT = dynamodb.Table(DDB_TABLE_NAME)


@retry(wait=wait_random_exponential(), stop=stop_after_delay(15))
def _get_item(item_id):
    '''Put record item'''
    result = DDT.get_item(
        Key={
            DDB_TABLE_HASH_KEY: item_id
        }
    )

    return result.get('Item', {})


def handler(event, context):
    '''Function entry'''
    _logger.debug('Event received: {}'.format(json.dumps(event)))

    item_id = event['pathParameters']['id']
    item = _get_item(item_id)

    resp = {
        'statusCode': 200,
        'body': json.dumps(item)
    }
    _logger.debug('Response: {}'.format(json.dumps(resp)))
    return resp


