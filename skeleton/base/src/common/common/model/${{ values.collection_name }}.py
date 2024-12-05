from dataclasses import dataclass
from typing import Optional
from uuid import uuid4 as uuid

@dataclass
class Base${{ values.collection_name_cap }}Data:
    '''Base attributes of ${{ values.collection_name_cap }} type'''
    pass


@dataclass
class ${{ values.collection_name_cap }}Data(Base${{ values.collection_name_cap }}Data):
    '''${{ values.collection_name_cap }} data'''
    id: Optional[str] = None

@dataclass
class ${{ values.collection_name_cap }}ItemKeys:
    '''${{ values.collection_name_cap }} DDB item keys'''
    pk: str
    sk: str

    def get_data(self):
        return { k:v for (k, v) in self.__dict__.items() if k not in ${{ values.collection_name_cap }}ItemKeys.__dict__.keys() }

@dataclass
class ${{ values.collection_name_cap }}Item(${{ values.collection_name_cap }}Data, ${{ values.collection_name_cap }}ItemKeys):
    '''${{ values.collection_name_cap }} DDB item'''
    id: str

    def get_data(self):
        return { k:v for (k, v) in self.__dict__.items() if k not in ['sk', 'pk'] }

def create_keys(_id: Optional[str] = None) -> ${{ values.collection_name_cap }}ItemKeys:
    '''Create keys for DDB'''
    key = _id or str(uuid())
    return ${{ values.collection_name_cap }}ItemKeys(**{'pk': key, 'sk': key})

def get_keys(_id: str) -> ${{ values.collection_name_cap }}ItemKeys:
    '''Get keys for DDB'''
    return ${{ values.collection_name_cap }}ItemKeys(**{'pk': _id, 'sk': _id})