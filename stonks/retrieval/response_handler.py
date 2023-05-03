"""Handle API responses."""

from requests.models import Response

from stonks.data_storage.storage import DataStorage


def handle_response(output_path, response: Response):
    if response.ok:
        DataStorage.write_json(output_path, response.json())
        print(f"Successfully wrote output to {output_path}.")
    else:
        raise ValueError(
            f"Endpoint {response.url} responded with non-200 status code '{response.status_code}'. Full response: {response.json()}"
        )
