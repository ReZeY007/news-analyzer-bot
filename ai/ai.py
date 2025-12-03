from os import getenv
from gigachat import GigaChat
from gigachat.models import Messages, MessagesRole


giga = GigaChat(credentials=getenv('GIGACHAT_KEY'),
                verify_ssl_certs=False,
                model='GigaChat-2',
                )

SYSTEM_PROMPT = 'Ты бот-анализатор новостей. Твоя задача проанализировать общий эмоциональный окрас новостей, выделить ключевые слова и написать краткую сводку.'
messages = [Messages(role=MessagesRole.SYSTEM, content=SYSTEM_PROMPT)]


async def ai_request(message):
    resp = await giga.achat(message)
    answer = resp.choices[0].message.content
    
    return answer


async def analyze_news(news: dict) -> dict:
    pass