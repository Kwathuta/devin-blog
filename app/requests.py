import requests, json

api_url = None


def configure_request(app):
    global api_url
    api_url = app.config["API_URL"]


def get_quotes():
    """
    function to get quotes from api
    """
    response = requests.get(api_url)
    if response.status_code == 200:
        quote = response.json()
        return quote
