'''Test ${{ values.function_name}}'''
{%- if values.event_source_type == 's3' -%}
{% set event_data_source_class = 'S3Event' -%}
{% elif values.event_source_type == 'sns' -%}
{% set event_data_source_class = 'SNSEvent' -%}
{% elif values.event_source_type == 'sqs' -%}
{% set event_data_source_class = 'SQSEvent' -%}
{% elif values.event_source_type == 'eventbridge' -%}
{% set event_data_source_class = 'EventBridgeEvent' -%}
{% elif values.event_source_type == 'cloudwatch_alarm' -%}
{% set event_data_source_class = 'CloudWatchAlarmEvent' -%}
{% elif values.event_source_type == 'cloudwatch_log' -%}
{% set event_data_source_class = 'CloudWatchLogsEvent' -%}
{% elif values.event_source_type == 'config' -%}
{% set event_data_source_class = 'AWSConfigRuleEvent' -%}
{% else %}
{% set event_data_source_class = 'Event' %}
{%- endif %}
from dataclasses import asdict
import json
import jsonschema
import os
from types import ModuleType
from typing import Generator

import pytest
from pytest_mock import MockerFixture

import boto3
# NOTE: uncomment following line if function calls AWS services and see AWS Clients below
#from moto import mock_aws
{% if values.event_data_type_name -%}
from aws_lambda_powertools.utilities.data_classes import ${{ event_data_source_class }}
{% endif -%}
from aws_lambda_powertools.utilities.typing import LambdaContext

from common.model.${{ values.event_data_type_name }} import ${{ values.event_data_type_name }}Data
from common.test.aws import create_lambda_function_context

from src.handlers.${{ values.function_name }}.function import Output${{ ', Event' if not values.event_source_type }}


FN_NAME = '${{ values.function_name }}'
DATA_DIR = './data'
FUNC_DATA_DIR = os.path.join(DATA_DIR, 'handlers', FN_NAME)
EVENT = os.path.join(FUNC_DATA_DIR, 'event.json')
EVENT_SCHEMA = os.path.join(FUNC_DATA_DIR, 'event.schema.json')
DATA = os.path.join(FUNC_DATA_DIR, 'data.json')
DATA_SCHEMA = os.path.join(FUNC_DATA_DIR, 'data.schema.json')
OUTPUT = os.path.join(FUNC_DATA_DIR, 'output.json')
OUTPUT_SCHEMA = os.path.join(FUNC_DATA_DIR, 'output.schema.json')

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
# Event
@pytest.fixture()
def mock_event(e=EVENT) -> ${{ values.event_data_source_class }}:
    '''Return a function event'''
    with open(e) as f:
        return ${{ values.event_data_type_name }}(json.load(f))

@pytest.fixture()
def event_schema(schema=EVENT_SCHEMA):
    '''Return an event schema'''
    with open(schema) as f:
        return json.load(f)

# Output
@pytest.fixture()
def mock_expected_output(output=OUTPUT) -> Output:
    '''Return a function output'''
    with open(output) as f:
        return Output(**json.load(f))

@pytest.fixture()
def expected_output_schema(output_schema=OUTPUT_SCHEMA):
    '''Return an output schema'''
    with open(output_schema) as f:
        return json.load(f)

# AWS Clients
#
# NOTE: uncomment aws_credentials() and mocked_aws() if function calls AWS services. Then see
#  mock_s3_client() as an example of mocking an AWS service. Be sure to pass your mocked AWS
#  client to your tests.
#
# Mocking AWS services must also be done before importing the function.
#
#@pytest.fixture()
#def aws_credentials() -> None:
#    '''Mocked AWS Credentials for moto.'''
#    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
#    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
#    os.environ["AWS_SECURITY_TOKEN"] = "testing"
#    os.environ["AWS_SESSION_TOKEN"] = "testing"
#    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
#
#@pytest.fixture()
#def mocked_aws(aws_credentials):
#    '''Mock all AWS interactions'''
#    with mock_aws():
#        yield
#
#@pytest.fixture()
#def mock_s3_client(mocked_aws) -> Generator[S3Client, None, None]:
#    '''Return a mocked S3 client'''
#    s3_client = boto3.client('s3')
#    s3_client.create_bucket(Bucket='MockBucket')
#    yield s3_client

# Function
@pytest.fixture()
def mock_context(function_name=FN_NAME):
    '''context object'''
    return create_lambda_function_context(function_name)

@pytest.fixture()
def mock_fn(mocker: MockerFixture) -> Generator[ModuleType, None, None]:
    '''Return mocked function'''
    import src.handlers.CreateThingItem.function as fn

    # NOTE: use mocker to mock any top-level variables outside of the handler function.
    # eg.
    #mocker.patch(
    #    'src.handlers.${{ values.function_name }}.function.DDB_TABLE_NAME',
    #    'MockTableName'
    #)

    yield fn


### Data validation tests
def test_validate_data(mock_data, data_schema):
    '''Test data against schema'''
    jsonschema.Draft7Validator(asdict(mock_data), data_schema)

def test_validate_event(mock_event, event_schema):
    '''Test event against schema'''
    jsonschema.Draft7Validator(mock_event._data, event_schema)

def test_validate_expected_data(mock_expected_output, expected_output_schema):
    '''Test output against schema'''
    jsonschema.Draft7Validator(asdict(mock_expected_output), expected_output_schema)


### Code Tests
def test__main(mock_data: ${{ values.event_data_type_name_cap }}Data):
    '''Test _main function'''
    r = mock_fn._main(mock_data)
    assert r is None


def test_handler(
    mock_fn: ModuleType,
    mock_context,
    mock_event: ${{ event_data_source_class }},
    mock_data: ${{ values.event_data_type_name_cap }}Data,
    mock_expected_output: Output,
):
    '''Test calling handler'''
    # Call the function
    response = mock_fn.handler(mock_event, mock_context)
    assert response == mock_expected_output