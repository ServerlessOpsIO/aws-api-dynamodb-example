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
dynamodb = boto3.resource('dynamodb')
DDT = dynamodb.Table(DDB_TABLE_NAME)


@retry(wait=wait_random_exponential(), stop=stop_after_delay(28))
def _put_item(item):
    '''Put record item'''
    resp = DDT.put_item(
        TableName=DDB_TABLE_NAME,
        Item=item
    )

    return resp


def handler(event, context):
    '''Function entry'''
    _logger.debug('Event received: {}'.format(json.dumps(event)))

    resp_list = []
    for r in event.get('Records', []):
        item = json.loads(r.get('body'))
        resp = _put_item(item)
        resp_list.append(resp)

    _logger.debug('Responses: {}'.format(json.dumps(resp_list)))

    return resp_list

