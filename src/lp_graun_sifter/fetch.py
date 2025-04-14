from pprint import pprint
import os
import sys

import dotenv
import requests

dotenv.load_dotenv()


def fetch(search: str, date_from: str = None) -> list[dict]:
    '''
    search:
        The string to search for. 
    date_from (optional):
        Allows the user to fetch only results later than the given date. Must be in the format YYYY-MM-DD.
    '''
    query = "https://content.guardianapis.com/search?"
    if date_from:
        query += f"from-date={date_from}&"
    query += f"q={search}&api-key={os.environ['GRAUN_API_KEY']}"

    response = requests.get(query, timeout=5)

    results = response.json()['response']['results']
    keys_to_select = ["webPublicationDate", "webTitle", "webUrl"]
    selected_results = [{key: value for key, value in result.items() \
                         if key in keys_to_select} for result in results]
    
    return selected_results


if __name__ == "__main__":
    pprint(fetch(sys.argv[1], sys.argv[2]))
