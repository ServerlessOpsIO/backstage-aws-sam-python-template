'''Create ${{ values.collection_name_cap }}'''

import json
import os
from dataclasses import asdict

import boto3
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.utilities.data_classes import event_source, APIGatewayProxyEvent
from aws_lambda_powertools.utilities.typing import LambdaContext
from mypy_boto3_dynamodb import DynamoDBServiceResource
from mypy_boto3_dynamodb.service_resource import Table
from mypy_boto3_dynamodb.type_defs import PutItemInputTablePutItemTypeDef

from common.model.${{ values.collection_name }} import ${{ values.collection_name_cap }}Data, ${{ values.collection_name_cap }}ItemKeys, ${{ values.collection_name_cap }}Item, get_keys
from common.util.dataclasses import lambda_dataclass_response
from .types import Output, ResponseBody

LOGGER = Logger(utc=True)

DDB: DynamoDBServiceResource = boto3.resource('dynamodb', 'us-east-1')
DDB_TABLE: Table = DDB.Table(os.environ.get('DDB_TABLE_NAME', ''))


def _upsert_item(item_keys: ${{ values.collection_name_cap }}ItemKeys, item_data: ${{ values.collection_name_cap }}Data) -> None:
    '''Upsert a ${{ values.collection_name_cap }} in DDB'''
    item = ${{ values.collection_name_cap }}Item(
        **{
            **asdict(item_keys),
            **asdict(item_data)
        }
    )

    ddb_put_item_args: PutItemInputTablePutItemTypeDef = {
        'Item': asdict(item),
        'ConditionExpression': 'attribute_exists(pk) AND attribute_exists(sk)'
    }

    DDB_TABLE.put_item(**ddb_put_item_args)

    return


@LOGGER.inject_lambda_context
@event_source(data_class=APIGatewayProxyEvent)
@lambda_dataclass_response
def handler(event: APIGatewayProxyEvent, context: LambdaContext) -> Output:
    '''Upsert function entry'''
    LOGGER.debug('Event', extra={"message_object": event.raw_event})

    body = event.body or '{}'
    item_keys = get_keys(event.path_parameters.get('id', ''))
    item_data = ${{ values.collection_name_cap }}Data(**json.loads(body))
    _upsert_item(item_keys, item_data)

    response_body = ResponseBody(
        **{
            "request_id": context.aws_request_id
        }
    )

    output = Output(statusCode=201, body=json.dumps(asdict(response_body)))

    LOGGER.debug('Output', extra={"message_object": asdict(output)})
    return output