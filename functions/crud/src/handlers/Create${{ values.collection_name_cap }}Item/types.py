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
    '''Creation API Response body'''
    id: str
