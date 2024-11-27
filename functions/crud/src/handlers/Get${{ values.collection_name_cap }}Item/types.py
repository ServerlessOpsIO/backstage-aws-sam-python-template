'''
Function dataclasses
'''
from dataclasses import dataclass

from common.model.${{ values.collection_name }} import ${{ values.collection_name_cap }}Data

@dataclass
class Output:
    '''Function response'''
    statusCode: int
    body: str

@dataclass
class ResponseBody(${{ values.collection_name_cap }}Data):
    '''API Response body'''

@dataclass
class ErrorResponseBody():
    '''API error response body'''
    error: str
    message: str