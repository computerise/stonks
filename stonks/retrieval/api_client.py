"""API Clients."""

import requests
from retrieval.request_builder import Request


class APIClient:
    def __init__(self):
        pass

    def get(self, request: Request):
        return requests.get(request.url, headers=request.headers).json()
