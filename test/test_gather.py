import boto3
from unittest.mock import Mock, patch

from src.lp_graun_sifter import gather


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


# def test_fetch_invoked():


# def test_post_invoked_with_results_matching_search():


# def test_valid_response_dict_received():
#     # assert response type is dict
#     # assert contains 'Successful' or 'Failed'
#     # assert num of Successful/Failed messages sums to total fetched
#     # assert contains 'ResponseMetaData' with 'HTTPStatusCode'
