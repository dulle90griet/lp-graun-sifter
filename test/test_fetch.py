from unittest.mock import Mock, patch
import pytest

from src.lp_graun_sifter.fetch import fetch


@pytest.fixture
def sample_response():
    return {
        "response": {
            "currentPage": 1,
            "orderBy": "relevance",
            "pageSize": 10,
            "pages": 3,
            "results": [
                {
                    "apiUrl": "https://content.guardianapis.com/artanddesign/2023/nov/26/the-big-picture-brian-graham-robert-frank-raoul-hague-goin-down-the-road",
                    "id": "artanddesign/2023/nov/26/the-big-picture-brian-graham-robert-frank-raoul-hague-goin-down-the-road",
                    "isHosted": False,
                    "pillarId": "pillar/arts",
                    "pillarName": "Arts",
                    "sectionId": "artanddesign",
                    "sectionName": "Art and design",
                    "type": "article",
                    "webPublicationDate": "2023-11-26T07:00:12Z",
                    "webTitle": "The big picture: artists Robert Frank, Raoul Hague and a lost bohemia",
                    "webUrl": "https://www.theguardian.com/artanddesign/2023/nov/26/the-big-picture-brian-graham-robert-frank-raoul-hague-goin-down-the-road"
                },
                {
                    "apiUrl": "https://content.guardianapis.com/artanddesign/2025/jan/05/the-big-picture-irene-poon-chocolate-bars-1965",
                    "id": "artanddesign/2025/jan/05/the-big-picture-irene-poon-chocolate-bars-1965",
                    "isHosted": False,
                    "pillarId": "pillar/arts",
                    "pillarName": "Arts",
                    "sectionId": "artanddesign",
                    "sectionName": "Art and design",
                    "type": "article",
                    "webPublicationDate": "2025-01-05T07:00:14Z",
                    "webTitle": "The big picture: every chocoholic’s "
                                "dream?",
                    "webUrl": "https://www.theguardian.com/artanddesign/2025/jan/05/the-big-picture-irene-poon-chocolate-bars-1965"
                },
                {
                    "apiUrl": "https://content.guardianapis.com/artanddesign/2025/mar/30/ken-grant-welsh-valleys-cwm-a-fair-country-photography",
                    "id": "artanddesign/2025/mar/30/ken-grant-welsh-valleys-cwm-a-fair-country-photography",
                    "isHosted": False,
                    "pillarId": "pillar/arts",
                    "pillarName": "Arts",
                    "sectionId": "artanddesign",
                    "sectionName": "Art and design",
                    "type": "article",
                    "webPublicationDate": "2025-03-30T09:00:15Z",
                    "webTitle": "‘People have walked through here for centuries’: the rhythms of the Welsh valleys in pictures",
                    "webUrl": "https://www.theguardian.com/artanddesign/2025/mar/30/ken-grant-welsh-valleys-cwm-a-fair-country-photography"
                }],
            "startIndex": 1,
            "status": "ok",
            "total": 30,
            "userTier": "developer"}
    }


@pytest.fixture
def requests_get_patcher(sample_response):
    response_mock = Mock()
    response_mock.json.return_value = sample_response
    patcher = patch("src.lp_graun_sifter.fetch.requests.get", return_value = response_mock)
    patcher.start()
    yield patcher
    patcher.stop()


def test_required_fields_appear_expected_num_of_times_in_fetched_data(requests_get_patcher):
    str_of_return = str(fetch("test_search"))
    assert str_of_return.count("webPublicationDate") == 3
    assert str_of_return.count("webTitle") == 3
    assert str_of_return.count("webUrl") == 3


def test_fetch_returns_list_of_dicts_containing_only_expected_fields(requests_get_patcher):
    fetched_json = str(fetch("a_search_string"))
    assert isinstance(fetched_json, list)
    for result in fetched_json:
        assert isinstance(result, dict)
        keys = result.keys()
        assert len(keys) == 3
        assert "webPublicationDate" in keys
        assert "webTitle" in keys
        assert "webUrl" in keys
    

# def test_raises_error_on_timeout(sample_response):

