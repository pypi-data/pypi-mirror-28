import time
from boto.connection import AWSAuthConnection
from boto.exception import BotoClientError
from boto.provider import Provider
from elasticsearch.exceptions import ConnectionError
from elasticsearch.connection.base import Connection as BaseConnection

class BotoConnection(AWSAuthConnection, BaseConnection):
    AuthServiceName = 'es'
    def __init__(self, host, **kwargs):
        provider = Provider('aws', access_key=kwargs.get('access_key'), secret_key=kwargs.get('secret_key'))
        super(BotoConnection, self).__init__(provider=provider, host=host)

    def _required_auth_capability(self):
        return ['hmac-v4']

    def perform_request(self, method, url, params=None, body=None, timeout=None, ignore=(), headers=None):
        start = time.time()
        data = body or ''
        try:
            response = self.make_request(method, url, headers=headers, host=self.host, data=data, auth_path=url)
        except Exception as e:
            self.log_request_fail(method, url, url, body, time.time() - start, exception=e)
            if isinstance(e, BotoClientError):
                raise ConnectionError('N/A', str(e), e)

        return response.status, dict(response.msg.items()), response.read().decode('utf-8')