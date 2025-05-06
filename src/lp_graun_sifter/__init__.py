"""Defines gather(), the interface for the module's integrated functionality."""

import os
import sys
from pprint import pprint

import boto3
import dotenv

from .fetch import fetch
from .post import post


def gather(
    sqs_client: boto3.client,
    sqs_queue_url: str,
    search_string: str,
    date_from: str = None,
    api_key: str = None,
) -> dict:
    """Fetches results from the Guardian API and sends them to an SQS queue.

    Args:
        sqs_client:
            The boto3 client to be used to connect to SQS.
        sqs_queue_url:
            The string of the target SQS queue's URL.
        search_string:
            The search string to be provided to the Guardian API.
        date_from (optional):
            A string in the format "YYYY-MM-DD". If provided, only results
            later than this date will be requested from the API.

    Returns:
        A dict containing:
        - "Fetched":
            A list of articles fetched. Each article is represented by a dict
            with "webPublicationDate", "webTitle", "webUrl" and "contentPreview" keys.
        - Response data received from SQS:
            At present, this comprises the keys "Successful", "Failed", and
            "ResponseMetadata". For more information, see https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/client/send_message_batch.html.

        Returned IDs of successful posts to SQS end in a number from 0 to 9.
        These numbers correspond to the indices of items in the "Fetched" list.
    """

    # If the API key is not provided, fetch it from environment variables
    if not api_key:
        try:
            api_key = os.environ["GUARDIAN_API_KEY"]
        except KeyError as e:
            raise RuntimeError(
                "GUARDIAN_API_KEY environment variable not found. Please "
                "supply api_key to gather() on invocation, or provide it via "
                "environment variable."
            ) from e

    # Retrieve the articles with fetch(), then send them with post()
    fetch_results = fetch(api_key, search_string, date_from)
    response = post(sqs_client, sqs_queue_url, fetch_results)

    # Add the fetched articles to the response dict received from SQS
    response.update({"Fetched": fetch_results})
    return response


def main(sqs_client: boto3.client = None) -> None:
    """The command-line entry point."""

    # Hydrate the environment with our locally stored API key
    dotenv.load_dotenv()

    # Fetch arguments from the command line
    sqs_queue_url = sys.argv[1]
    search_string = sys.argv[2]
    try:
        date_from = sys.argv[3]
    except IndexError:
        date_from = None

    # If AWS_REGION isn't defined in the environment, get it from the session
    try:
        aws_region = os.environ["AWS_REGION"]
    except KeyError:
        aws_region = boto3.Session().region_name

    # Create the SQS client (if not injected for testing), and invoke gather()
    if not sqs_client:
        sqs_client = boto3.client("sqs", region_name=aws_region)
    response = gather(sqs_client, sqs_queue_url, search_string, date_from)

    pprint(response)


if __name__ == "__main__":  # pragma: no cover
    main()
