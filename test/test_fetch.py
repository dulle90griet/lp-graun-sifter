from unittest.mock import Mock, patch
import pytest
import requests
import json
import os

from src.lp_graun_sifter.fetch import fetch


@pytest.fixture
def sample_response():
    with open("test/data/sample_api_response.json", "r") as f:
        sample_json = json.loads(f.read())
    return sample_json


@pytest.fixture
def requests_get_patcher(sample_response):
    response_mock = Mock()
    response_mock.json.return_value = sample_response
    patcher = patch(
        "src.lp_graun_sifter.fetch.requests.get", return_value=response_mock
    )
    patcher.start()
    yield patcher
    patcher.stop()


@pytest.fixture
def test_api_key():
    saved_key = os.environ["GUARDIAN_API_KEY"]
    os.environ["GUARDIAN_API_KEY"] = "test"
    yield
    os.environ["GUARDIAN_API_KEY"] = saved_key


def test_query_string_well_formed(test_api_key):
    requests_get_spy = Mock(wraps=requests.get)
    with patch("src.lp_graun_sifter.fetch.requests.get", side_effect=requests_get_spy):
        fetch('"debussy on ice"')
        formed_query = requests_get_spy.call_args.args[0]
        assert (
            formed_query
            == 'https://content.guardianapis.com/search?q="debussy on ice"&order-by=newest&show-fields=body&api-key=test'
        )

        fetch('"pinwheel cantata"', date_from="2025-04-01")
        formed_query = requests_get_spy.call_args.args[0]
        assert (
            formed_query
            == 'https://content.guardianapis.com/search?from-date=2025-04-01&q="pinwheel cantata"&order-by=newest&show-fields=body&api-key=test'
        )


def test_required_fields_appear_expected_num_of_times_in_fetched_data(
    requests_get_patcher,
):
    str_of_return = str(fetch("test_search"))
    assert str_of_return.count("webPublicationDate") == 3
    assert str_of_return.count("webTitle") == 3
    assert str_of_return.count("webUrl") == 3
    assert str_of_return.count("contentPreview") == 3


def test_fetch_returns_list_of_dicts_containing_only_expected_fields(
    requests_get_patcher,
):
    fetched_json = fetch("a_search_string")
    assert isinstance(fetched_json, list)
    for result in fetched_json:
        assert isinstance(result, dict)
        keys = result.keys()
        assert len(keys) == 4
        assert "webPublicationDate" in keys
        assert "webTitle" in keys
        assert "webUrl" in keys
        assert "contentPreview" in keys


def test_content_previews_of_expected_length(requests_get_patcher):
    fetched_json = fetch("test meridian")
    for result in fetched_json:
        assert 0 < len(result["contentPreview"]) <= 1000


def test_results_ordered_by_date_desc():
    results = fetch("keir starmer", date_from="2025-04-10")
    for i in range(len(results) - 1):
        assert results[i]["webPublicationDate"] > results[i + 1]["webPublicationDate"]


# def test_raises_error_on_timeout(sample_response):
