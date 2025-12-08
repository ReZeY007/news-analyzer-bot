from os import getenv
from newsdataapi import NewsDataApiClient
import json

from ai.ai import analyze_news as ai_analyze

api = NewsDataApiClient(apikey=getenv('NEWS_API_KEY'))


def get_news(topic: str, size: int = 5) -> list:
    response = api.latest_api(qInTitle=topic, language='ru', size=size)

    if response['status'] == 'success':
        news = response['results']
    else:
        raise Exception('NewsDataAPI error')
    
    return news


async def analyze_news(news: dict):
    prepared_news = list()
    news_string = str()

    for n in news:
        prepared_news.append(f'Заголовок:\n{n['title']}\nОписание:\n{n['description']}\nКлючевые слова:\n{n['keywords']}\n\n')

    for n in prepared_news:
        news_string += n    

    print(prepared_news)
    response = await ai_analyze(news_string)
    response = json.loads(response)


    return response
    