from unicodedata import normalize
from aiogram.utils.formatting import Text, Bold, TextLink


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


def format_analyzis(news: dict) -> Text:
    sentiment = news['sentiment']
    keywords = ', '.join(news['keywords'])
    summary = news['summary']

    formated_news = Text('Эмоциональный окрас: ', Bold(sentiment), '\n' +
                         'Ключевые слова: ', Bold(keywords), '\n' * 2 +
                         summary)

    return formated_news
