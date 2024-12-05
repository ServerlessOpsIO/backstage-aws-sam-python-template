from dataclasses import dataclass
from typing import Optional
from uuid import uuid4 as uuid

COLLECTION_NAME = '${{ values.collection_name }}'

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

def create_keys() -> ${{ values.collection_name_cap }}ItemKeys:
    '''Create keys for DDB'''
    key = '{}#{}'.format(COLLECTION_NAME, str(uuid()))
    return ${{ values.collection_name_cap }}ItemKeys(**{'pk': key, 'sk': key})

def get_keys_from_id_from_id(_id: str) -> ${{ values.collection_name_cap }}ItemKeys:
    '''Get keys for DDB'''
    key = '{}#{}'.format(COLLECTION_NAME, _id)
    return ${{ values.collection_name_cap }}ItemKeys(**{'pk': key, 'sk': key})

def get_id_from_keys(keys: ${{ values.collection_name_cap }}ItemKeys) -> str:
    '''Get id from keys'''
    return keys.pk.split('#')[1]