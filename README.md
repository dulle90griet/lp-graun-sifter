# lp_graun_sifter

_Graun Sifter_ is a Python library enabling AWS applications to search for _Guardian_ articles, posting matches to a message broker. It has been tested on Python versions 3.9–13 and on both x86_64 and amd64 Lambda architectures. Its name is a reference to _Grauniad_, the nickname given to the paper by the writers of _Private Eye_ magazine on account of the _Guardian_'s legendarily poor standards of copyediting.

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

Tests are run prior to each commit. Should you wish to run them yourself to double-check for vulnerabilities, however, you can do so using:

```sh
make run-checks
```

Finally, generate the Lambda layer .zip file:

```sh
make build-lambda-layer
```

The layer file will be created in the packages/ directory. It can now be uploaded to AWS Lambda and added to your serverless Lambda function, either by using the browser console, the AWS CLI, or an infrastructure-as-code manager like Terraform.

For more information about configuring Lambda layers, consult the following links:

- [Creating and deleting layers](https://docs.aws.amazon.com/lambda/latest/dg/creating-deleting-layers.html)
- [Adding layers](https://docs.aws.amazon.com/lambda/latest/dg/adding-layers.html)

### Configuring your environment

You will need a _Guardian_ API key, available [here](https://open-platform.theguardian.com/access/). Your API key can then be provided to your Lambda function as an [environment variable](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html) (`GUARDIAN_API_KEY`) or using [AWS Secrets Manager](https://docs.aws.amazon.com/lambda/latest/dg/with-secrets-manager.html). For security reasons, it is not recommended to reproduce the API key directly in your source code.

The role associated with any Lambda function that invokes the _Graun Sifter_ module will need to be granted appropriate permissions for SQS: at minimum, `SQS:SendMessage` and `SQS:ReceiveMessage`. You will also need to ensure that the role is added to the destination SQS queue's [access policy](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-overview-of-managing-access.html), associating the role's ARN with the `SQS:SendMessage` action (if the queue was created in the console, this will usually come under the SID "__sender_statement") and the `SQS:ReceiveMessage` action (in the console, usually under the SID "__receiver_statement").

## Using the module

### Integrating _Graun Sifter_ into a Lambda function

Once the layer is added to your Lambda function, the module can be imported as normal:

```python
include lp_graun_sifter as gs
```

The core interface with _Graun Sifter_ is the `gs.gather()` function, which takes the arguments:

- `sqs_client`: The [boto3 client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html) to be used to connect to SQS.
- `sqs_queue_url`: The string of the target SQS queue's URL.
- `search_string`: The search string to be provided to the Guardian API.
- `date_from` (optional): A string in the format "YYYY-MM-DD". If provided, only results later than this date will be requested from the API.
- `api_key`(optional): A string variable containing your _Guardian_ API key, if first retrieved from Secrets Manager. If not provided, _Graun Sifter_ will default to attempting to access the `GUARDIAN_API_KEY` environment variable.

The _Guardian_ API is queried for the most recent articles matching the search terms, up to a maximum of 10 articles. For each, a JSON object with the fields "webPublicationDate", "webTitle", "webUrl" and "contentPreview" (the first 1,000 characters of the article body) is then sent to the SQS queue for later retrieval.

`gs.gather()` returns a dict containing the [response data](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/client/send_message_batch.html) received from SQS, as well as a key, `Fetched`, whose value is a list of dicts containing the data of the articles sent to SQS.

### Calling _Graun Sifter_ from the command line

If you need to test your API key and SQS queue configuration prior to setting up a Lambda function, _Graun Sifter_ can be invoked from the command line. In this mode of operation, it's expected that your API key will be provided via the `GUARDIAN_API_KEY` environment variable.

Create a file named `.env` in the root directory of your local copy of this repository, and add the line:

```sh
GUARDIAN_API_KEY="your_api_key_here"
```

If this is your first time running the script, set up the local dev environment.

```sh
make create-environment && make dev-setup
source ./venv/bin/activate
```

Ensure that your [AWS credentials](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html) are set up locally, and that the correct AWS account is activated. The easiest way to do this is to install the [AWS CLI](http://aws.amazon.com/cli/) and use its interactive `configure` command to set up your credentials and default region:

```sh
aws configure
```

To confirm which role is currently active, use:

```sh
aws sts get-caller-identity
```

To switch AWS profile when multiple profiles are configured locally, check `~/.aws/credentials` for the bracketed `[profile_name]` and use:

```sh
export AWS_PROFILE=profile_name
```

Finally, with your environment configured, the library can be invoked as follows, again working from the repository's root directory:

```sh
export PYTHONPATH=$(pwd)
python src/lp_graun_sifter https://your.sqs/queue/url "your search string" 2023-01-01
```

As elsewhere, the final date argument is optional.
