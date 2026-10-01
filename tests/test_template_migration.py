from pathlib import Path


def test_template_migrates_from_boto3_stubs_to_types_boto3():
    pipfile = Path('skeleton/base/Pipfile').read_text()
    templates = [
        Path('functions/crud/src/handlers/Get${{ values.collection_name_cap }}Item/function.py').read_text(),
        Path('functions/event_handler/src/handlers/${{ values.function_name }}/function.py').read_text(),
    ]

    assert 'types-boto3' in pipfile
    assert 'boto3-stubs' not in pipfile
    assert 'types_boto3_dynamodb' in ''.join(templates)
    assert 'types_boto3_s3' in ''.join(templates)
