"""Defines gather(), the interface for the module's integrated functionality."""

import os
import boto3

from .fetch import fetch
from .post import post


def gather(sqs_client: boto3.client, sqs_queue_url: str, search_string: str, date_from: str=None) -> dict:
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
            "ResponseMetaData". For more information, see https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/client/send_message_batch.html.
        
        Returned IDs of successful posts to SQS end in a number from 0 to 9.
        These numbers correspond to the indices of items in the "Fetched" list.
    """

    api_key = os.environ["GUARDIAN_API_KEY"]
    fetch_results = fetch(api_key, search_string, date_from)
    response = post(sqs_client, sqs_queue_url, fetch_results)
    response.update({"Fetched": fetch_results})
    return response


if __name__ == "__main__":
    import sys
    import dotenv

    dotenv.load_dotenv()

    sqs_queue_url = sys.argv[1]
    search_string = sys.argv[2]
    try:
        date_from = sys.argv[3]
    except IndexError:
        date_from = None

    try:
        aws_region = os.environ["AWS_REGION"]
    except KeyError:
        aws_region = boto3.Session().region_name

    sqs_client = boto3.client("sqs", region_name=aws_region)

    response = gather(sqs_client, sqs_queue_url, search_string, date_from)
    print(response)
