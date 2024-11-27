'''
Function dataclasses
'''
from dataclasses import dataclass

@dataclass
class Output:
    '''Function response'''
    statusCode: int
    body: str


@dataclass
class ResponseBody:
    '''API Response body'''
    request_id: str