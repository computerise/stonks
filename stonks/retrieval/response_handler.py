"""Handle API responses."""

import logging
from pathlib import Path
from requests.models import Response

from stonks.error_handler import raise_fatal_error
from stonks.storage import DataStorage


def handle_response(output_path: Path, response: Response, store: bool = True):
    if response.ok:
        if store:
            DataStorage.write_json(output_path, response.json())
            logging.info(f"Successfully wrote output to {output_path}.")
    else:
        raise_fatal_error(
            f"Endpoint {response.url} responded with non-200 status code '{response.status_code}'. Full response: {response.json()}",
        )
