'''Test ${{ values.function_name}}'''
{%- if values.event_source_type == 's3' -%}
{%- set event_data_source_class = 'S3Event' -%}
{%- set mock_client_name = 'mock_s3_client' -%}
{%- elif values.event_source_type == 'sns' -%}
{%- set event_data_source_class = 'SNSEvent' -%}
{%- elif values.event_source_type == 'sqs' -%}
{%- set event_data_source_class = 'SQSEvent' -%}
{%- elif values.event_source_type == 'eventbridge' -%}
{%- set event_data_source_class = 'EventBridgeEvent' -%}
{%- elif values.event_source_type == 'cloudwatch_alarm' -%}
{%- set event_data_source_class = 'CloudWatchAlarmEvent' -%}
{%- elif values.event_source_type == 'cloudwatch_log' -%}
{%- set event_data_source_class = 'CloudWatchLogsEvent' -%}
{%- elif values.event_source_type == 'config' -%}
{%- set event_data_source_class = 'AWSConfigRuleEvent' -%}
{%- else %}
{%- set event_data_source_class = 'Event' %}
{%- endif %}

{%- if values.destination_type == 's3' -%}
{%- set mock_client_name = 'mock_s3_client' -%}
{%- set mock_resource_identifier = 'mock_s3_bucket_name' -%}
{%- set mypy_module = 'mypy_boto3_s3' -%}
{%- set mypy_client_class = 'S3Client' -%}
{%- set destination_env_var = 'S3_BUCKET_NAME' -%}
{%- elif values.destination_type == 'sns' -%}
{%- set mock_client_name = 'mock_sns_client' -%}
{%- set mock_resource_identifier = 'mock_sns_topic_name' -%}
{%- set mypy_module = 'mypy_boto3_sns' -%}
{%- set mypy_client_class = 'SNSClient' -%}
{%- set destination_env_var = 'SNS_TOPIC_ARN' -%}
{%- elif values.destination_type == 'sqs' -%}
{%- set mock_client_name = 'mock_sqs_client' -%}
{%- set mock_resource_identifier = 'mock_sqs_queue_url' -%}
{%- set mypy_module = 'mypy_boto3_sqs' -%}
{%- set mypy_client_class = 'SQSClient' -%}
{%- set destination_env_var = 'SQS_QUEUE_URL' -%}
{%- elif values.destination_type == 'eventbridge' -%}
{%- set mock_client_name = 'mock_eventbridge_client' -%}
{%- set mock_resource_identifier = 'mock_event_bus_name' -%}
{%- set mypy_module = 'mypy_boto3_events' -%}
{%- set mypy_client_class = 'EventBridgeClient' -%}
{%- set destination_env_var = 'EVENT_BUS_NAME' -%}
{% endif %}
from dataclasses import asdict
import json
import jsonschema
import os
from types import ModuleType
from typing import Generator

import pytest
from pytest_mock import MockerFixture

{% if values.destination_type -%}
import boto3
from ${{ mypy_module }} import ${{ mypy_client_class }}
from moto import mock_aws
{% endif %}
{% if values.event_source_type -%}
from aws_lambda_powertools.utilities.data_classes import ${{ event_data_source_class }}
{% endif -%}
from aws_lambda_powertools.utilities.typing import LambdaContext

from common.model.${{ values.event_data_type_name }} import ${{ values.event_data_type_name_cap }}Data
from common.test.aws import create_lambda_function_context
{% if not values.event_source_type %}from src.handlers.${{ values.function_name }}.function import Event{% endif %}

FN_NAME = '${{ values.function_name }}'
DATA_DIR = './data'
FUNC_DATA_DIR = os.path.join(DATA_DIR, 'handlers', FN_NAME)
EVENT = os.path.join(FUNC_DATA_DIR, 'event.json')
EVENT_SCHEMA = os.path.join(FUNC_DATA_DIR, 'event.schema.json')
DATA = os.path.join(FUNC_DATA_DIR, 'data.json')
DATA_SCHEMA = os.path.join(FUNC_DATA_DIR, 'data.schema.json')

### Fixtures
# Data
@pytest.fixture()
def mock_data(data=DATA) -> ${{ values.event_data_type_name_cap }}Data:
    '''Return function event data'''
    with open(data) as f:
        return ${{ values.event_data_type_name_cap }}Data(**json.load(f))

@pytest.fixture()
def data_schema(data_schema=DATA_SCHEMA):
    '''Return a data schema'''
    with open(data_schema) as f:
        return json.load(f)

# FIXME: Need to handle differences between powertools event classes and the Event class
# Event
@pytest.fixture()
def mock_event(e=EVENT) -> ${{ event_data_source_class }}:
    '''Return a function event'''
    with open(e) as f:
        return ${{ event_data_source_class }}(json.load(f))

@pytest.fixture()
def event_schema(schema=EVENT_SCHEMA):
    '''Return an event schema'''
    with open(schema) as f:
        return json.load(f)

{% if values.destination_type %}
# AWS Clients
#
# NOTE: Mocking AWS services must also be done before importing the function.
@pytest.fixture()
def aws_credentials() -> None:
    '''Mocked AWS Credentials for moto.'''
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture()
def mocked_aws(aws_credentials):
    '''Mock all AWS interactions'''
    with mock_aws():
        yield

{% if values.event_source_type == 's3' or values.destination_type == 's3' %}
@pytest.fixture()
def ${{ mock_client_name }}(mocked_aws) -> Generator[${{ mypy_client_class }}, None, None]:
    '''Create a mock client'''
    s3_client = boto3.client('s3')
    yield s3_client

def ${{ mock_resource_identifier }}(${{ mock_client_name }}) -> str:
    '''Create a mock resource'''
    mock_bucket_name = 'MockBucket'
    mock_s3_client.create_bucket(Bucket=mock_bucket_name)
    return mock_bucket_name

{%- elif values.destination_type == 'sns' %}
@pytest.fixture()
def ${{ mock_client_name }}(mocked_aws) -> Generator[${{ mypy_client_class }}, None, None]:
    sns_client = boto3.client('sns')
    yield sns_client

def ${{ mock_resource_identifier }}(${{ mock_client_name }}) -> str:
    '''Create a mock resource'''
    mock_topic_name = 'MockTopic'
    mock_sns_client.create_topic(Name=mock_topic_name)
    return mock_topic_name

{%- elif values.destination_type == 'sqs' -%}
@pytest.fixture()
def ${{ mock_client_name }}(mocked_aws) -> Generator[${{ mypy_client_class }}, None, None]:
    sqs_client = boto3.client('sqs')
    yield sqs_client

def ${{ mock_resource_identifier }}(${{ mock_client_name }}) -> str:
    '''Create a mock resource'''
    mock_queue_name = 'MockQueue'
    r = mock_sqs_client.create_queue(QueueName=mock_queue_name)
    return r['QueueUrl']

{%- elif values.destination_type == 'eventbridge' -%}
@pytest.fixture()
def ${{ mock_client_name }}(mocked_aws) -> Generator[${{ mypy_client_class }}, None, None]:
    eventbridge_client = boto3.client('events')
    yield eventbridge_client

def ${{ mock_resource_identifier }}(${{ mock_client_name }}) -> str:
    '''Create a mock resource'''
    mock_bus_name = 'MockBus'
    eventbridge_client.create_event_bus(Name=mock_bus_name)
    return mock_bus_name
{%- endif %}
{% endif %}

# Function
@pytest.fixture()
def mock_context(function_name=FN_NAME):
    '''context object'''
    return create_lambda_function_context(function_name)

@pytest.fixture()
def mock_fn(
{% if mock_resource_identifier %}    ${{ mock_resource_identifier }}: str,{% endif %}
    mocker: MockerFixture
) -> Generator[ModuleType, None, None]:
    '''Return mocked function'''
    import src.handlers.${{ values.function_name }}.function as fn

    # NOTE: use mocker to mock any top-level variables outside of the handler function.
    mocker.patch(
        'src.handlers.${{ values.function_name }}.function.${{ destination_env_var }}',
        ${{ mock_resource_identifier }}
    )

    yield fn


### Data validation tests
def test_validate_data(mock_data, data_schema):
    '''Test data against schema'''
    jsonschema.Draft7Validator(asdict(mock_data), data_schema)

# FIXME: Need to handle differences between powertools event classes and the Event class
def test_validate_event(mock_event, event_schema):
    '''Test event against schema'''
    jsonschema.Draft7Validator(mock_event._data, event_schema)


### Code Tests
def test__main(
    mock_fn: ModuleType,
    mock_data: ${{ values.event_data_type_name_cap }}Data
):
    '''Test _main function'''
    mock_fn._main(mock_data)


def test_handler(
    mock_fn: ModuleType,
    mock_context,
    mock_event: ${{ event_data_source_class }},
    mock_data: ${{ values.event_data_type_name_cap }}Data,
    {% if mock_client_name %}${{ mock_client_name }}: ${{ mypy_client_class }},{% endif %}
):
    '''Test calling handler'''
    # Call the function
    mock_fn.handler(mock_event, mock_context)