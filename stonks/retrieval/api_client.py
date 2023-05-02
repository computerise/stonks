"""API Clients."""

import requests
from retrieval.request_builder import Request


class APIClient:
    """API client used for sending requests."""

    def __init__(self):
        """Initialise class instance."""
        pass

    def get(self, request: Request):
        """Get the specified request and return the response as a JSON object."""
        return requests.get(
            request.url, headers=request.headers, params=request.query_string
        ).json()
