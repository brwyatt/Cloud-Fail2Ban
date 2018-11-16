import pytest

import F2B.dynamo as dynamo


@pytest.fixture(autouse=True)
def mock_dynamo_table_put_item(monkeypatch):
    def mock(*args, **kwargs):
        return {
            'ResponseMetadata': {
                'RetryAttempts': 0,
                'HTTPHeaders': {
                    'content-type': 'application/x-amz-json-1.0',
                    'server': 'Server',
                    'connection': 'keep-alive',
                    'x-amz-crc32': '11111',
                    'date': 'Mon, 01 Jan 2018 01:02:30 GMT',
                    'content-length': '2',
                    'x-amzn-requestid': 'XXXXXXXXXX'
                },
                'RequestId': 'XXXXXXX',
                'HTTPStatusCode': 200
            }
        }
    monkeypatch.setattr(dynamo.table, 'put_item', mock)


@pytest.fixture
def mock_dynamo_table_put_item_exception(monkeypatch):
    def mock(*args, **kwargs):
        raise Exception('Something happened!')
    monkeypatch.setattr(dynamo.table, 'put_item', mock)


@pytest.fixture
def mock_dynamo_table_put_item_http_error(monkeypatch):
    def mock(*args, **kwargs):
        return {
            'ResponseMetadata': {
                'RetryAttempts': 0,
                'HTTPHeaders': {
                    'content-type': 'application/x-amz-json-1.0',
                    'server': 'Server',
                    'connection': 'keep-alive',
                    'x-amz-crc32': '11111',
                    'date': 'Mon, 01 Jan 2018 01:02:30 GMT',
                    'content-length': '2',
                    'x-amzn-requestid': 'XXXXXXXXXX'
                },
                'RequestId': 'XXXXXXX',
                'HTTPStatusCode': 500
            }
        }
    monkeypatch.setattr(dynamo.table, 'put_item', mock)


@pytest.fixture(autouse=True)
def mock_dynamo_table_query(monkeypatch):
    def mock(*args, **kwargs):
        return {
            'Items': []
        }
    monkeypatch.setattr(dynamo.table, 'query', mock)
