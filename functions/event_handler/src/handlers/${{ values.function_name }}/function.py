{%- if values.function_description %}
'''${{ values.function_description }}'''
{%- endif %}

{%- if values.event_source_type == 's3' -%}
{%- set event_data_source_class = 'S3Event' -%}
{%- set data_type_class = "${{ values.event_data_type_name_cap }}Data" -%}

{%- elif values.event_source_type == 'sns' -%}
{%- set event_data_source_class = 'SNSEvent' -%}
{%- set data_type_class = "${{ values.event_data_type_name_cap }}Data" -%}

{%- elif values.event_source_type == 'sqs' -%}
{%- set event_data_source_class = 'SQSEvent' -%}
{%- set data_type_class = "${{ values.event_data_type_name_cap }}Data" -%}

{%- elif values.event_source_type == 'eventbridge' -%}
{%- set event_data_source_class = 'EventBridgeEvent' -%}
{%- set data_type_class = "${{ values.event_data_type_name_cap }}Data" -%}

{%- elif values.event_source_type == 'cloudwatch_alarm' -%}
{%- set event_data_source_class = 'CloudWatchAlarmEvent' -%}

{%- elif values.event_source_type == 'cloudwatch_log' -%}
{%- set event_data_source_class = 'CloudWatchLogsEvent' -%}

{%- elif values.event_source_type == 'config' -%}
{%- set event_data_source_class = 'AWSConfigRuleEvent' -%}

{%- endif %}

{%- if values.destination_type == 's3' -%}
{% set mypy_client_class = 'S3Client' -%}

{% elif values.destination_type == 'sns' -%}
{% set mypy_client_class = 'SNSClient' -%}

{% elif values.destination_type == 'sqs' -%}
{% set mypy_module = 'mypy_boto3_sqs' -%}
{% set mypy_client_class = 'SQSClient' -%}

{% elif values.destination_type == 'eventbridge' -%}
{% set mypy_client_class = 'EventBridgeClient' -%}

{% endif -%}

{%- if values.destination_type %}
import os
{%- endif %}
{%- if not values.event_source_type %}
from dataclasses import dataclass
{%- endif %}
{%- if values.event_source_type == 's3' %}
from typing import TYPE_CHECKING
{%- endif %}

{%- if values.destination_type %}
import boto3

{%- if values.event_source_type == 's3' %}
if TYPE_CHECKING:
    from mypy_boto3_s3.type_defs import GetObjectOutputTypeDef
{%- endif %}
{%- endif %}

from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
{%- if values.event_source_type %}
from aws_lambda_powertools.utilities.data_classes import (
    event_source,
    ${{ event_data_source_class }}
)
{%- endif %}

from common.model.${{ values.event_data_type_name }} import ${{ values.event_data_type_name_cap }}Data

LOGGER = Logger(utc=True)
{# Initialize AWS clients #}
{%- if values.event_source_type == 's3' %}
S3_CLIENT = boto3.client('s3')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'UNSET')
{%- endif %}
{%- if values.destination_type == 's3' and not values.event_source_type == 's3' %}
S3_CLIENT = boto3.client('s3')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'UNSET')
{%- elif values.destination_type == 'sns' %}
SNS_CLIENT = boto3.client('sns')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'UNSET')
{%- elif values.destination_type == 'sqs' %}
SQS_CLIENT = boto3.client('sqs')
SQS_QUEUE_URL = os.environ.get('SQS_QUEUE_URL', 'UNSET')
{%- elif values.destination_type == 'eventbridge' %}
EVENTBRIDGE_CLIENT = boto3.client('events')
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME', 'UNSET')
{%- endif %}

{# Common client tasks #}
{%- if values.event_source_type == 'ddb' %}
def _put_ddb_item(item_data: ${{ values.event_data_type_name_cap }}Data) -> None:
    '''Put item in DynamoDB'''
    pass

{%- elif values.event_source_type == 's3' %}
def _get_s3_object(bucket: str, key: str) -> 'GetObjectOutputTypeDef':
    '''Get object from S3'''
    # NOTE: 'GetObjectOutputTypeDef' needs to be quoted to work with it's earlier conditional
    # import. This is called a type hint Forward Reference
    return S3_CLIENT.get_object(Bucket=bucket, Key=key)


def _get_s3_object_contents(bucket: str, key: str) -> str:
    '''Get object from S3'''
    obj = S3_CLIENT.get_object(Bucket=bucket, Key=key)
    return obj['Body'].read().decode()

{%- endif %}

def _main(data: ${{ values.event_data_type_name_cap }}Data) -> None:
    '''Main work of function'''
    # Transform data

    # Send data to destination

    return


@LOGGER.inject_lambda_context
{%- if not event_data_source_class %}
def handler(event, context: LambdaContext) -> None:
{%- else %}
@event_source(data_class=${{ event_data_source_class }})
def handler(event: ${{ event_data_source_class }}, context: LambdaContext) -> None:
{%- endif %}
    '''Event handler'''
    LOGGER.debug('Event', extra={"message_object": event})

{#- Call _main() by event source type #}
{% if values.event_source_type == 's3' %}
    for record in event.records:
        _main(record)
{%- elif values.event_source_type == 'sns' %}
    for record in event.records:
        _main(record.sns.message)
{%- elif values.event_source_type == 'sqs' %}
    for record in event.records:
        _main(record.body)
{%- elif values.event_source_type == 'eventbridge' %}
    _main(event.detail)
{%- elif values.event_source_type == 'cloudwatch_alarm' %}
    _main(event.alarm_data)
{%- elif values.event_source_type == 'cloudwatch_log' %}
    decompressed_log: CloudWatchLogsDecodedData = event.parse_logs_data()
    for log_event in decompressed_log.log_events:
        _main(log_event)
{%- elif values.event_source_type == 'config' %}
    _main(event)
{%- endif %}

    return
