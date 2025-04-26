from src.lp_graun_sifter.fetch import fetch
from src.lp_graun_sifter.post import post


def gather(search_string, date_from, sqs_client, sqs_queue_url):
    fetch_results = fetch(search_string, date_from)
    response = post(sqs_client, sqs_queue_url, fetch_results)
    return response


if __name__ == "__main__":
    import sys
    import dotenv

    dotenv.load_dotenv()

    # search_string = 