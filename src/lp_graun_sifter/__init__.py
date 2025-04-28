import os
import boto3

from .fetch import fetch
from .post import post


def gather(sqs_client, sqs_queue_url, search_string, date_from=None) -> dict:
    fetch_results = fetch(search_string, date_from)
    response = post(sqs_client, sqs_queue_url, fetch_results)
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
