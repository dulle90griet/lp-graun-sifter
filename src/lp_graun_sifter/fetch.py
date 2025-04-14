from pprint import pprint
import os
import sys

import dotenv
import requests

dotenv.load_dotenv()
api_key = os.environ['GRAUN_API_KEY']


def fetch(search: str, date_from: str = None) -> dict:
    '''
    search:
        The string to search for. 
    date_from (optional):
        Allows the user to fetch only results later than the given date. Must be in the format YYYY-MM-DD.
    '''
    query = "https://content.guardianapis.com/search?"
    if date_from:
        query += f"from-date={date_from}&"
    query += f"q={search}&api-key={api_key}"

    response = requests.get(query, timeout=5)

    results = response.json()['response']['results']
    keys_to_select = ["webPublicationDate", "webTitle", "webUrl"]
    selected_results = []
    for result in results:
        result_dict = {}
        for key, value in result.items():
            if key in keys_to_select:
                result_dict[key] = value
        selected_results.append(result_dict)
        
    return selected_results


if __name__ == "__main__":
    pprint(fetch(sys.argv[1], sys.argv[2]))




# We grow them the old-fashioned way: from an apple's
# seed. Yes, just one for many. Well, they sprout.
# They shoot. Have no sense of wonder. Then they're off.
