import urllib.request, json
from .models import Quote

api_url = None


def configure_request(app):
    global api_url
    api_url = app.config["API_URL"]


def get_quotes():
    """
    function to get quotes from api
    """
    with urllib.request.urlopen(api_url) as url:
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)

        quotes_results = None

        if get_quotes_response["quotes"]:
            quotes_results_list = get_quotes_response["quotes"]
            quotes_results = process_quotes_results(quotes_results_list)
    return quotes_results


def process_quotes_results(quotes_list):
    """
    Function to process the quotes result and turn them to a list of objects
    Args:
        quotes_list: A list of dictionaries to contain sources details
    Returns:
        quotes_results: A list of sources objects
    """
    quotes_results = []
    for quotes_item in quotes_list:
        author = quotes_item.get("author")
        id = quotes_item.get("id")
        quote = quotes_item.get("quote")
        permalink = quotes_item.get("permalink")

        quotes_object = Quote(author, id, quote, permalink)

        quotes_results.append(quotes_object)
    return quotes_results
