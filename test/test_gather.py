import os
from unittest.mock import patch
import pytest
import json
from moto import mock_aws
import boto3

from src.lp_graun_sifter.__init__ import gather, main
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

    saved_key = os.environ.get("GUARDIAN_API_KEY", "")
    os.environ["GUARDIAN_API_KEY"] = "test"
    yield
    os.environ["GUARDIAN_API_KEY"] = saved_key


@pytest.fixture(scope="function")
def sample_fetch_output():
    """Loads sample fetch() output data for use in mocking"""

    with open("test/data/sample_fetch_output.json", "r", encoding="utf8") as f:
        return json.loads(f.read())


def test_gather_invokes_fetch_once_with_given_search_and_date(
    sqs, test_api_key, sample_fetch_output
):
    """Checks that gather() invokes fetch() with the provided arguments"""

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
    sqs, test_api_key, sample_fetch_output
):
    """Checks that gather() invokes post() with the messages returned by fetch()"""

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


def test_gather_returns_valid_response_dict(sqs, test_api_key, sample_fetch_output):
    """Checks that gather() returns a dict with the expected key structure"""

    # Load known sample SQS responses for use in mocking post()
    with open("test/data/sample_post_output_1.json", "r", encoding="utf8") as f:
        sample_post_output_1 = json.loads(f.read())
    with open("test/data/sample_post_output_2.json", "r", encoding="utf8") as f:
        sample_post_output_2 = json.loads(f.read())

    # Define a helper function to keep this test DRY
    def act_and_assert():
        response = gather(sqs, queue_url, "Apple announce", "2025-01-01")

        assert isinstance(response, dict)
        assert "Fetched" in response
        assert len(response["Fetched"]) == 3
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


def test_gather_raises_informative_error_if_no_api_key_provided(sqs, test_api_key):
    """Checks that gather() raises the expected error if api_key is not provided
    and no GUARDIAN_API_KEY env variable exists.
    """

    expected_err = (
        "GUARDIAN_API_KEY environment variable not found. Please "
        "supply api_key to gather() on invocation, or provide it via "
        "environment variable."
    )
    queue_url = sqs.create_queue(QueueName="test-sqs-queue")["QueueUrl"]

    # Delete the existing env variable
    del os.environ["GUARDIAN_API_KEY"]

    # Patch load_dotenv to prevent hydration
    with patch("src.lp_graun_sifter.__init__.dotenv.load_dotenv"):
        with pytest.raises(RuntimeError) as err:
            gather(sqs, queue_url, "a search that won't be searched")


def test_main_invokes_gather_once_with_command_line_args(
    sqs, test_api_key, sample_fetch_output
):
    """Checks that main() invokes gather() with the arguments supplied by the CLI"""

    # Define dummy args to simulate command-line invocation
    test_args = [
        "src/lp_graun_sifter",
        "https://a.queue.url",
        "search string",
        "2023-01-01",
    ]

    with patch("src.lp_graun_sifter.__init__.sys.argv", test_args):
        with patch("src.lp_graun_sifter.__init__.gather") as gather_mock:
            gather_mock.return_value = None

            main(sqs)

            gather_mock.assert_called_once_with(
                sqs, "https://a.queue.url", "search string", "2023-01-01"
            )


def test_main_prints_response_with_expected_features(
    sqs, test_api_key, sample_fetch_output, capsys
):
    """Checks that main()'s printed output features all of the expected dict keys"""

    queue_url = sqs.create_queue(QueueName="test-sqs-queue")["QueueUrl"]

    # Define dummy args to simulate command-line invocation
    test_args = ["src/lp_graun_sifter", queue_url, "search string"]

    with patch("src.lp_graun_sifter.__init__.sys.argv", test_args):
        with patch("src.lp_graun_sifter.__init__.fetch") as fetch_mock:
            fetch_mock.return_value = sample_fetch_output

            main(sqs)

    captured = capsys.readouterr().out
    assert "Fetched" in captured
    for article in sample_fetch_output:
        assert article["webPublicationDate"] in captured
        assert article["webTitle"][:10] in captured
        assert article["webUrl"] in captured
        assert article["contentPreview"][:10] in captured
    assert "Successful" in captured
    assert "Failed" in captured
    assert "ResponseMetadata" in captured
    assert "HTTPStatusCode" in captured
