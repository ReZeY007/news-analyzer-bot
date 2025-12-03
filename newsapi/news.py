from os import getenv
from unicodedata import normalize
from newsdataapi import NewsDataApiClient
from aiogram.utils.formatting import Text, Bold, TextLink

api = NewsDataApiClient(apikey=getenv('NEWS_API_KEY'))


def get_news(topic: str, size: int = 5) -> list:
    response = api.latest_api(qInTitle=topic, language='ru', size=size)

    if response['status'] == 'success':
        news = response['results']
    else:
        raise Exception('NewsDataAPI error')
    
    return news

# transforms news (one article) dictionary to aiogram's Text object
def format_news(news: dict) -> Text:
    title = ''
    description = ''
    link = ''
    if news['title']:
        title = normalize('NFC', news['title'])
    if news['description']:
        description = normalize('NFC', news['description'])
    if news['link']:
        link = news['link']
    
    text = Text(Bold(title) + ' (' + TextLink('Ссылка', url=link) + ')' + '\n' * 2, description)
    return text