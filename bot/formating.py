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


def format_analyzis():
    pass