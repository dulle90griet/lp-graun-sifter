"""Defines the post() function."""

from datetime import datetime, timezone
import json


def post(client, queue_url: str, messages: list[dict]) -> dict:
    """Sends up to 10 articles to the specified SQS queue.

    Takes a list of JSON messages and constructs a list of Entries (dicts with
    the keys "Id" and "MessageBody") before sending them to the SQS queue with
    the URL provided.

    Args:
        client:
            The botocore.client.SQS instance to use to connect to AWS SQS.
        queue_url:
            A string giving the HTTPS endpoint of the SQS queue.
        messages:
            The list of message dicts to be posted to the queue.

    Returns:
        The response data received by SQS, namely a dict with the keys
        "ResponseMetadata" and either or both of "Successful" and "Failed".
        For more information, see https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/client/send_message_batch.html.
    """

    # Construct a string of the current datetime to prefix message IDs
    cur_time = datetime.now(timezone.utc)
    id_prefix = cur_time.strftime("%Y%m%dT%H%M%S_")

    # Cap number of messages at 10
    if len(messages) > 10:
        messages = messages[:10]

    # Construct the list of entries
    entries = [
        {
            "Id": f"{id_prefix}{i}",
            "MessageBody": json.dumps(message, ensure_ascii=False),
        }
        for i, message in enumerate(messages)
    ]

    # Send the batch
    response = client.send_message_batch(QueueUrl=queue_url, Entries=entries)

    return response
