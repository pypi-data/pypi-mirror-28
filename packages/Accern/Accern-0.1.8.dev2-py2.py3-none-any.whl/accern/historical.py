"""Python library for Accern API.

Core client functionality, common across all API requests (including performing
HTTP requests).
"""

from accern import default_client, error, util
from accern.schema import Schema
from accern.default_client import AccernClient

API_BASE = "https://admin-staging.accern.com/api/io/jobs"


class HistoricalClient(AccernClient):
    """Perform requests to the Accern API web services."""

    def __init__(self, token=None, client=None):
        """Intialize with params.

        :param client: default http client. Optional
        :param token: Accern API token. Required.
        """
        self.api_base = API_BASE
        self.token = token
        self._client = client or default_client.new_http_client()

    @staticmethod
    def interpret_response(rbody, rcode, rheaders):
        try:
            if hasattr(rbody, 'decode'):
                rbody = rbody.decode('utf-8')
            resp = util.json.loads(rbody)
        except Exception:
            raise error.APIError(
                "Invalid response body from API: %s "
                "(HTTP response code was %d)" % (rbody, rcode),
                rbody, rcode, rheaders)

        if not 200 <= rcode < 300:
            raise AccernClient.handle_error(rbody, rcode, resp)

        return resp

    def create_job(self, schema):
        """Create a job with schema.

        :param schema: job detail, will be added to payload

        :raises ApiError: when the API returns an error.
        :raises Timeout: if the request timed out.
        :raises TransportError: when something went wrong while trying to
            exceute a request.
        """

        schema = Schema.validate_schema(method='historical', schema=schema)
        token = AccernClient.check_token(self.token)
        method = 'POST'

        headers = AccernClient.build_api_headers(token, method)

        if method == 'POST':
            post_data = util.json.dumps({'query': schema})
        else:
            post_data = None

        rbody, rcode, rheaders = self._client.request(method, self.api_base, headers, post_data)
        resp = self.interpret_response(rbody, rcode, rheaders)
        return resp

    def get_jobs(self, job_id=None):
        """Get the user's job history.

        :param job_id: if job_id is valid, will return the job related
        """

        token = AccernClient.check_token(self.token)
        method = 'GET'
        headers = AccernClient.build_api_headers(token, method)
        if job_id is None:
            rbody, rcode, rheaders = self._client.request(method, self.api_base, headers, post_data=None)
            resp = self.interpret_response(rbody, rcode, rheaders)
        else:
            rbody, rcode, rheaders = self._client.request(method, '%s/%s' % (self.api_base, job_id), headers, post_data=None)
            resp = self.interpret_response(rbody, rcode, rheaders)

        return resp
