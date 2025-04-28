import os
from unittest.mock import Mock, patch
import pytest
import requests
import re
from moto import mock_aws
import boto3

from pprint import pprint

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
    """Return a mocked SQS client"""
    with mock_aws():
        yield boto3.client("sqs", region_name="eu-west-2")


@pytest.fixture
def test_api_key():
    saved_key = os.environ["GUARDIAN_API_KEY"]
    os.environ["GUARDIAN_API_KEY"] = "test"
    yield
    os.environ["GUARDIAN_API_KEY"] = saved_key


def test_fetch_invoked_once(sqs, test_api_key):
    with patch('src.lp_graun_sifter.__init__.fetch', wraps=fetch) as spy_fetch:
        queue_url = sqs.create_queue(QueueName="test-sqs-queue")["QueueUrl"]
        gather(sqs, queue_url, "test search")
        
        spy_fetch.assert_called_once_with("test search", None)


def test_post_invoked_with_results_matching_search(sqs, test_api_key):
    with patch('src.lp_graun_sifter.__init__.post', wraps=post) as spy_post:
        queue_url = sqs.create_queue(QueueName="test-sqs-queue")["QueueUrl"]
        search_str = "grimsby diner"

        gather(sqs, queue_url, search_str)

        # Test for invocation
        spy_post.assert_called_once()

        # Test for plausible relevance of results
        # Search terms may appear in the article but not in the fields we're
        # selecting, so fetch each full article until one doesn't match
        posted_results = spy_post.call_args.args[2]
        # Search pattern provides a rule of thumb, but doesn't account for
        # grouping of words enclosed in quotes
        clean_search = re.sub(r"[^(\w\s)]", "", search_str)
        search_pattern = f"({"|".join(clean_search.split())})"
        keyword_present_in_all_results = True
        for result in posted_results:
            query = result["webUrl"].replace(
                "www.theguardian.com",
                "content.guardianapis.com"
            ) + f"?api-key={os.environ["GUARDIAN_API_KEY"]}&show-fields=all"
            response = requests.get(query, timeout=5)
            fields = response.json()['response']['content']['fields']

            if not re.search(search_pattern, str(fields).lower()):
                keyword_present_in_all_results = False
                break
            
        assert keyword_present_in_all_results


# def test_valid_response_dict_received():
#     # assert response type is dict
#     # assert contains 'Successful' or 'Failed'
#     # assert num of Successful/Failed messages sums to total fetched
#     # assert contains 'ResponseMetaData' with 'HTTPStatusCode'
