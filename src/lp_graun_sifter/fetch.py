"""Defines the fetch() function."""

import requests


def fetch(api_key: str, search: str, date_from: str = None) -> list[dict]:
    """Fetches up to 10 articles matching the search term from the Guardian API.

    Queries the Guardian API using the given API key, search string and
    optional date_from argument, retrieving the most recent articles (up to 10)
    that match the search, before extracting and returning the relevant fields
    from each article's content in the format expected by post().

    Args:
        search:
            The string to search for.
        date_from (optional):
            Allows the user to fetch only results later than the given date.
            Must be in the format "YYYY-MM-DD".

    Returns:
        A list of up to 10 dicts, each containing a single fetched article's
        "webPublicationDate", "webTitle", "webUrl" and the first 1000
        characters of its "contentPreview" under keys of the same names.
    """

    # Construct the query to the Guardian API
    query = "https://content.guardianapis.com/search?"
    if date_from:
        query += f"from-date={date_from}&"
    query += f"q={search}&order-by=newest&show-fields=body&api-key={api_key}"

    # Make the query using GET and keep the response
    response = requests.get(query, timeout=5)

    # Extract the desired fields from the API response
    results = response.json()["response"]["results"]
    selected_results = [
        {
            "webPublicationDate": result["webPublicationDate"],
            "webTitle": result["webTitle"],
            "webUrl": result["webUrl"],
            "contentPreview": result["fields"]["body"][
                : min(len(result["fields"]["body"]), 1000)
            ],
        }
        for result in results
    ]

    return selected_results
