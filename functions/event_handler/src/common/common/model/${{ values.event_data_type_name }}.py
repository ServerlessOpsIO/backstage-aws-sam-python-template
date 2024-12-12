from dataclasses import dataclass
{%- if values.has_ddb %}
from uuid import uuid4 as uuid
{%- endif %}

COLLECTION_NAME = '${{ values.event_data_type_name }}'

@dataclass
class ${{ values.event_data_type_name_cap }}Data:
    '''${{ values.event_data_type_name_cap }} data'''
    pass

{%- if values.has_ddb %}
@dataclass
class ${{ values.event_data_type_name_cap }}ItemKeys:
    '''${{ values.event_data_type_name_cap }} DDB item keys'''
    pk: str
    sk: str

    def get_data(self):
        return { k:v for (k, v) in self.__dict__.items() if k not in ${{ values.collection_name_cap }}ItemKeys.__dict__.keys() }

@dataclass
class ${{ values.event_data_type_name_cap }}Item(${{ values.event_data_type_name_cap }}Data, ${{ values.event_data_type_name_cap }}ItemKeys):
    '''${{ values.event_data_type_name_cap }} DDB item'''

    def get_data(self):
        return { k:v for (k, v) in self.__dict__.items() if k not in ['sk', 'pk'] }

def create_keys() -> ${{ values.event_data_type_name_cap }}ItemKeys:
    '''Create keys for DDB'''
    key = '{}#{}'.format(COLLECTION_NAME, str(uuid()))
    return ${{ values.event_data_type_name_cap }}ItemKeys(**{'pk': key, 'sk': key})

def get_keys_from_id(_id: str) -> ${{ values.event_data_type_name_cap }}ItemKeys:
    '''Get keys for DDB'''
    key = '{}#{}'.format(COLLECTION_NAME, _id)
    return ${{ values.event_data_type_name_cap }}ItemKeys(**{'pk': key, 'sk': key})

def get_id_from_keys(keys: ${{ values.event_data_type_name_cap }}ItemKeys) -> str:
    '''Get id from keys'''
    return keys.pk.split('#')[1]
{% endif %}