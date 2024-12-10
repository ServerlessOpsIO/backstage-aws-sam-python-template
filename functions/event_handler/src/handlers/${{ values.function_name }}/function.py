{% if values.function_description %}'''${{ values.function_description }}'''{% endif %}

{%- if values.event_source_type == 's3' -%}
{% set event_data_source_class = 'S3Event' -%}
{% set data_type_class = "${{ values.event_data_type_name_cap }}Data" -%}
{% elif values.event_source_type == 'sns' -%}
{% set event_data_source_class = 'SNSEvent' -%}
{% set data_type_class = "${{ values.event_data_type_name_cap }}Data" -%}
{% elif values.event_source_type == 'sqs' -%}
{% set event_data_source_class = 'SQSEvent' -%}
{% set data_type_class = "${{ values.event_data_type_name_cap }}Data" -%}
{% elif values.event_source_type == 'eventbridge' -%}
{% set event_data_source_class = 'EventBridgeEvent' -%}
{% set data_type_class = "${{ values.event_data_type_name_cap }}Data" -%}
{% elif values.event_source_type == 'cloudwatch_alarm' -%}
{% set event_data_source_class = 'CloudWatchAlarmEvent' -%}
{% elif values.event_source_type == 'cloudwatch_log' -%}
{% set event_data_source_class = 'CloudWatchLogsEvent' -%}
{% elif values.event_source_type == 'config' -%}
{% set event_data_source_class = 'AWSConfigRuleEvent' -%}
{% else %}
{% set event_data_source_class = 'Event' -%}
{%- endif %}
from dataclasses import asdict, dataclass
{% if values.event_source_type == 'ddb' -%}
import boto3
from mypy_boto3_dynamodb import DynamoDBServiceResource
{% elif values.event_source_type == 's3' -%}
import boto3
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import GetObjectOutputTypeDef
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
from common.util.dataclasses import lambda_dataclass_response

LOGGER = Logger(utc=True)

{#- Initialize AWS clients -#}
{% if values.event_source_type == 'ddb' -%}
DDB: DynamoDBServiceResource = boto3.resource('dynamodb', 'us-east-1')
DDB_TABLE = DDB.Table(os.environ.get('DDB_TABLE_NAME', ''))
{% elif values.event_source_type == 's3' %}
S3_CLIENT: S3Client = boto3.client('s3')
{% endif %}

{% if not values.event_source_type -%}
@dataclass
class Event:
    '''Function event'''
{% endif %}
@dataclass
class Output:
    '''Function output'''

{# Common client tasks -#}
{% if values.event_source_type == 'ddb' -%}
def _put_ddb_item(item_data: ${{ values.event_data_type_name_cap }}Data) -> None:
    '''Put item in DynamoDB'''
    pass
{% elif values.event_source_type == 's3' %}
def _get_s3_object(bucket: str, key: str) -> GetObjectOutputTypeDef:
    '''Get object from S3'''
    return S3_CLIENT.get_object(Bucket=bucket, Key=key)


def _get_s3_object_contents(bucket: str, key: str) -> str:
    '''Get object from S3'''
    obj = S3_CLIENT.get_object(Bucket=bucket, Key=key)
    return obj['Body'].read().decode()
{% endif %}

def _main(data: ${{ values.event_data_type_name_cap }}Data) -> None:
    '''Main work of function'''
    pass


@LOGGER.inject_lambda_context
@lambda_dataclass_response
{% if event_data_source_class -%}
def handler(event, context: LambdaContext) -> Output:
{%- else -%}
@event_source(data_class=${{ event_data_source_class }})
def handler(event: ${{ event_data_source_class }}, context: LambdaContext) -> Output:
{% endif -%}
    '''Event handler'''
    LOGGER.debug('Event', extra={"message_object": event})

{#- Call _main() by event source type #}
{% if values.event_source_type == 's3' %}
    for record in event.records:
        _main(record)
{% elif values.event_source_type == 'sns' %}
    for record in event.records:
        _main(record.sns.message)
{% elif values.event_source_type == 'sqs' %}
    for record in event.records:
        _main(record.body)
{% elif values.event_source_type == 'eventbridge' %}
    _main(event.detail)
{% elif values.event_source_type == 'cloudwatch_alarm' %}
    _main(event.alarm_data)
{% elif values.event_source_type == 'cloudwatch_log' %}
    decompressed_log: CloudWatchLogsDecodedData = event.parse_logs_data()
    for log_event in decompressed_log.log_events:
        _main(log_event)
{% elif values.event_source_type == 'config' %}
    _main(event)
{%- endif %}
    output = Output()

    LOGGER.debug('Output', extra={"message_object": asdict(output)})
    return output
