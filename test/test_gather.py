import os
from unittest.mock import Mock, patch
import pytest
import json
import requests
import re
from moto import mock_aws
import boto3

from src.lp_graun_sifter.__init__ import gather
from src.lp_graun_sifter.fetch import fetch
from src.lp_graun_sifter.post import post


@pytest.fixture
def aws_credentials():
    """Mocked AWS credentials for moto testing"""

    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture
def sqs(aws_credentials):
    """Yields a mocked SQS client"""

    with mock_aws():
        yield boto3.client("sqs", region_name="eu-west-2")


@pytest.fixture(scope="function")
def test_api_key():
    """Exports a placeholder API key for the duration of a given test"""

    saved_key = os.environ["GUARDIAN_API_KEY"]
    os.environ["GUARDIAN_API_KEY"] = "test"
    yield
    os.environ["GUARDIAN_API_KEY"] = saved_key


@pytest.fixture(scope="session")
def sample_fetch_output():
    """Loads and yields sample fetch() output data for use in mocking"""

    with open("test/data/sample_fetch_output.json", "r", encoding="utf8") as f:
        yield json.loads(f.read())


def test_gather_invokes_fetch_once_with_given_search_and_date(
    sqs,
    test_api_key,
    sample_fetch_output
):
    queue_url = sqs.create_queue(QueueName="test-sqs-queue")["QueueUrl"]

    with patch("src.lp_graun_sifter.__init__.fetch") as fetch_mock:
        fetch_mock.return_value = sample_fetch_output
        gather(sqs, queue_url, "test search")
        fetch_mock.assert_called_once_with("test", "test search", None)

    with patch("src.lp_graun_sifter.__init__.fetch", wraps=fetch) as fetch_mock:
        fetch_mock.return_value = sample_fetch_output
        gather(sqs, queue_url, '"lord byron"', "1812-03-03")
        fetch_mock.assert_called_once_with("test", '"lord byron"', "1812-03-03")


def test_gather_invokes_post_once_with_output_of_fetch(
    sqs,
    test_api_key,
    sample_fetch_output
):
    queue_url = sqs.create_queue(QueueName="test-sqs-queue")["QueueUrl"]

    with patch("src.lp_graun_sifter.__init__.fetch") as fetch_mock:
        fetch_mock.return_value = sample_fetch_output

        with patch("src.lp_graun_sifter.__init__.post", wraps=post) as post_spy:
            gather(sqs, queue_url, "grimsby diner")
            post_spy.assert_called_once()
            posted_results = post_spy.call_args.args[2]
            assert posted_results == sample_fetch_output

        with patch("src.lp_graun_sifter.__init__.post", wraps=post) as post_spy:
            gather(sqs, queue_url, 'new model announce "MacBook Pro"')
            post_spy.assert_called_once()
            posted_results = post_spy.call_args.args[2]
            assert posted_results == sample_fetch_output


def test_gather_returns_valid_response_dict(
    sqs,
    test_api_key,
    sample_fetch_output
):
    # Load known sample SQS responses for use in mocking post()
    with open("test/data/sample_post_output_1.json", "r", encoding="utf8") as f:
        sample_post_output_1 = json.loads(f.read())
    with open("test/data/sample_post_output_2.json", "r", encoding="utf8") as f:
        sample_post_output_2 = json.loads(f.read())

    # Define a helper function to keep this test DRY
    def act_and_assert():
            response = gather(sqs, queue_url, "Apple announce", "2025-01-01")

            assert isinstance(response, dict)
            assert "Successful" in response or "Failed" in response
            messages_in_response = len(response.get("Successful", []))
            messages_in_response += len(response.get("Failed", []))
            assert messages_in_response == 3
            assert "ResponseMetadata" in response
            assert "HTTPStatusCode" in response["ResponseMetadata"]

    queue_url = sqs.create_queue(QueueName="test-sqs-queue")["QueueUrl"]

    with patch("src.lp_graun_sifter.__init__.fetch") as fetch_mock:
        fetch_mock.return_value = sample_fetch_output
 
        with patch("src.lp_graun_sifter.__init__.post", wraps=post) as post_mock:
            post_mock.return_value = sample_post_output_1
            act_and_assert()

            post_mock.return_value = sample_post_output_2
            act_and_assert()