from unittest.mock import Mock, patch
import pytest

from src.lp_graun_sifter.fetch import fetch


def test_fetch_returns_list_of_dicts_with_minimum_required_fields():
    response_mock = Mock()
    response_mock.json.return_value = {
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
    patcher = patch("src.lp_graun_sifter.fetch.requests.get", return_value = response_mock)

    patcher.start()
    fetched_json = fetch("test_search")
    fetched_str = str(fetched_json)
    assert fetched_str.count("webPublicationDate") == 3
    assert fetched_str.count("webTitle") == 3
    assert fetched_str.count("webUrl") == 3
    patcher.stop()
