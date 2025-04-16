from datetime import datetime, UTC
import sys
from copy import deepcopy
import json

import boto3


def post(client, queue_url: str, messages: list[dict]) -> None:
    '''
    client:
        The botocore.client.SQS instance to use to connect to AWS SQS.
    queue_url:
        The HTTPS endpoint of the SQS queue.
    messages:
        The list of message dicts to be posted to the queue.
    '''
    
    cur_time = datetime.now(UTC)
    id_prefix = cur_time.strftime("%Y%m%dT%H%M%S_")

    if len(messages) > 10:
        messages = messages[:10]

    entries = [{
        "Id": f"{id_prefix}{i}",
        "MessageBody": json.dumps(message, ensure_ascii=False)
    } for i, message in enumerate(messages)]

    response = client.send_message_batch(
        QueueUrl=queue_url,
        Entries=entries
    )

    return response


if __name__ == "__main__":
    region_name = sys.argv[1]
    queue_url = sys.argv[2]

    if len(sys.argv) > 3:
        messages = sys.argv[3]
    else:
        with open("test/data/sample_fetch_output.json", "r", encoding="utf8") as f:
            messages = json.loads(f.read())

    sqs = boto3.client('sqs', region_name=region_name)

    post(sqs, queue_url, messages)