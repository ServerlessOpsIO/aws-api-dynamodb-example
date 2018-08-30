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
SQS_QUEUE_URL = os.environ.get('SQS_QUEUE_URL')
SQS = boto3.client('sqs')


@retry(wait=wait_random_exponential(), stop=stop_after_delay(28))
def _send_message(msg):
    '''Put record item'''
    SQS.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=msg
    )


def handler(event, context):
    '''Function entry'''
    _logger.debug('Event received: {}'.format(json.dumps(event)))

    msg = event.get('body')
    _send_message(msg)

    resp = {
        'statusCode': 201,
        'body': json.dumps({'status': 'QUEUED'})
    }
    _logger.debug('Response: {}'.format(json.dumps(resp)))
    return resp

