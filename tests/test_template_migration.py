from pathlib import Path


def test_message_event_template_uses_types_boto3_cloudwatch_flag_names():
    template = Path('template-message-event-handler.yaml').read_text()
    pipfile = Path('skeleton/base/Pipfile').read_text()

    assert "has_cloudwatch_logs: ${{ true if parameters.event_source_type == 'cloudwatch_log' else false }}" in template
    assert "cloudwatch_event" not in template
    assert "has_cloudwatch_log:" not in template

    assert 'has_cloudwatch_logs' in pipfile
    assert 'has_cloudwatch_log:' not in template
