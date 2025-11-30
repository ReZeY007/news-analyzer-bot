from os import getenv
from newsdataapi import NewsDataApiClient

api = NewsDataApiClient(apikey=getenv('NEWS_API_KEY'))


def get_news(topic: str) -> list[dict]:
    response = api.latest_api(q=topic)

    if response['status'] == 'success':
        news = response['results']
    else:
        raise Exception('NewsDataAPI error')
    
    return news
