# lp_graun_sifter
A Python library enabling AWS applications to search for Guardian articles, posting matches to a message broker.

Currently, _Graun Sifter_ supports the Amazon SQS message queue.

## Installation and Setup

### Installing the module

From the directory of your choosing, clone this repository:

```sh
git clone https://www.github.com/lp_graun_sifter
```

Set up the project environment:

```sh
cd lp_graun_sifter
make create-environment
```

Generate the Lambda layer .zip file:

```sh
make build-lambda-layer
```

The layer file will be created in the packages/ directory. It can now be uploaded to AWS Lambda and added to your serverless Lambda function, either by using the browser console, the AWS CLI, or an infrastructure-as-code manager like Terraform.

For more information about configuring Lambda layers, consult the following links:

- [Creating and deleting layers](https://docs.aws.amazon.com/lambda/latest/dg/creating-deleting-layers.html)
- [Adding layers](https://docs.aws.amazon.com/lambda/latest/dg/adding-layers.html)

### Configuring your environment

You will need a _Guardian_ API key, available [here](https://open-platform.theguardian.com/access/). Your API key can then be provided to your Lambda function as an [environment variable](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html) (`GUARDIAN_API_KEY`) or using [AWS Secrets Manager](https://docs.aws.amazon.com/lambda/latest/dg/with-secrets-manager.html).

The role associated with any Lambda function that invokes the _Graun Sifter_ module will need to be granted appropriate permissions for SQS: at minimum, `SQS:SendMessage` and `SQS:ReceiveMessage`. You will also need to ensure that the role is added to the destination SQS queue's [access policy](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-overview-of-managing-access.html), associating the role's ARN with the `SQS:SendMessage` action (if the queue was created in the console, usually under the SID "__sender_statement") and the `SQS:ReceiveMessage` action (in the console, usually under the SID "__receiver_statement").

### Using the module

Once the layer is added to your Lambda function, the module can be included as normal within the function code:

```python
from lp_graun_sifter include gather
```

The core interface with _Graun Sifter_ is the `gather()` function, which takes the arguments:

- `sqs_client`: The boto3 client to be used to connect to SQS.
- `sqs_queue_url`: The string of the target SQS queue's URL.
- `search_string`: The search string to be provided to the Guardian API.
- `date_from` (optional): A string in the format "YYYY-MM-DD". If provided, only results later than this date will be requested from the API.
- `api_key`(optional): The string of your _Guardian_ API key, if first retrieved from Secrets Manager. If not provided, _Graun Sifter_ will default to attempting to access the `GUARDIAN_API_KEY` environment variable.

The _Guardian_ API is queried for the most recent articles matching the search terms, up to a maximum of 10 articles. For each, a JSON object with the fields "webPublicationDate", "webTitle", "webUrl" and "contentPreview" (the first 1,000 characters of the article body) is then sent to the SQS queue for later retrieval.

`gather()` returns a dict containing the [response data](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/client/send_message_batch.html) received from SQS, as well as a key, `Fetched`, whose value is a list of dicts containing the data of the articles sent to SQS.








