from unittest.mock import Mock, patch
import pytest
import requests
import json
import os

from src.lp_graun_sifter.fetch import fetch


@pytest.fixture
def sample_api_response(scope="function"):
    """Loads sample Guardian API response data for use in mocking"""
    with open("test/data/sample_api_response.json", "r") as f:
        return json.loads(f.read())


@pytest.fixture(scope="function")
def requests_get_patcher(sample_api_response):
    """Patches requests.get() to return a mock response object"""

    response_mock = Mock()
    response_mock.json.return_value = sample_api_response
    patcher = patch(
        "src.lp_graun_sifter.fetch.requests.get", return_value=response_mock
    )
    patcher.start()
    yield patcher
    patcher.stop()


@pytest.fixture(scope="function")
def test_api_key():
    """Exports a placeholder API key for the duration of a given test"""

    saved_key = os.environ.get("GUARDIAN_API_KEY", "")
    os.environ["GUARDIAN_API_KEY"] = "test"
    yield
    os.environ["GUARDIAN_API_KEY"] = saved_key


def test_fetch_generates_well_formed_query_string(test_api_key):
    """Checks that requests.get() is invoked with a query string generated in
    accordance with the Guardian API documentation at time of writing.
    """

    with patch("src.lp_graun_sifter.fetch.requests.get") as requests_get_mock:
        fetch("test", '"debussy on ice"')
        formed_query = requests_get_mock.call_args.args[0]
        assert (
            formed_query
            == 'https://content.guardianapis.com/search?q="debussy on ice"&order-by=newest&show-fields=body&api-key=test'
        )

        fetch("test", '"pinwheel cantata"', date_from="2025-04-01")
        formed_query = requests_get_mock.call_args.args[0]
        assert (
            formed_query
            == 'https://content.guardianapis.com/search?from-date=2025-04-01&q="pinwheel cantata"&order-by=newest&show-fields=body&api-key=test'
        )


def test_required_fields_appear_expected_num_of_times_in_fetched_data(
    requests_get_patcher,
):
    """Checks that fetch() returns as many of each required extracted field
    as there are messages in our patched API response data.
    """

    str_of_return = str(fetch("test", "test_search"))
    assert str_of_return.count("webPublicationDate") == 3
    assert str_of_return.count("webTitle") == 3
    assert str_of_return.count("webUrl") == 3
    assert str_of_return.count("contentPreview") == 3


def test_fetch_returns_list_of_dicts_containing_only_expected_fields(
    requests_get_patcher,
):
    """Checks the type of the return and confirms that no extraneous fields remain"""

    fetched_json = fetch("test", "a_search_string")
    assert isinstance(fetched_json, list)
    for result in fetched_json:
        assert isinstance(result, dict)
        keys = result.keys()
        assert len(keys) == 4
        assert "webPublicationDate" in keys
        assert "webTitle" in keys
        assert "webUrl" in keys
        assert "contentPreview" in keys


def test_fetch_returns_content_previews_of_expected_length(requests_get_patcher):
    """Checks that the contentPreview field is between 1 and 1000 characters long"""

    fetched_json = fetch("test", "test meridian")
    for result in fetched_json:
        assert 0 < len(result["contentPreview"]) <= 1000


def test_fetch_returns_results_ordered_by_date_desc():
    """Checks that fetch() returns results in order from newest to oldest"""

    results = fetch("test", "keir starmer", date_from="2025-04-10")
    for i in range(len(results) - 1):
        assert results[i]["webPublicationDate"] > results[i + 1]["webPublicationDate"]
