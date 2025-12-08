from os import getenv
from gigachat import GigaChat
from gigachat.models import Messages, MessagesRole, Chat


giga = GigaChat(credentials=getenv('GIGACHAT_KEY'),
                verify_ssl_certs=False,
                model='GigaChat-2',
                )

SYSTEM_PROMPT = 'Ты бот-анализатор новостей. Твоя задача, основываясь ТОЛЬКО на полученных данных, проанализировать общий эмоциональный окрас полученных новостей (от 0 до 1, где 0 - крайне негативно, 1 - крайне положительно) выделить ключевые словас (в виде текста, не пытайся вывести их ввиде unicode кодов) и написать краткую выжимку из новостей, как будто ты описываешь текущую ситуацию.\n Ответ должен быть СТРОГО в виде JSON-объекта следующего вида:\n {"sentiment": "эмоциональный окрас", "keywords": ["ключевое слово 1", "ключевое слово 2"], "summary": "общая информация"}\n Соблюдай все выше указанные правила и ничего не выдумывай'

payload = Chat(
    messages=[
        Messages(role=MessagesRole.SYSTEM, content=SYSTEM_PROMPT)
        ])


async def ai_request(message: str):
    payload.messages.append(Messages(role=MessagesRole.USER, content=message))

    resp = await giga.achat(message)
    answer = resp.choices[0].message.content

    payload.messages.pop()
    
    return answer


async def analyze_news(news: str) -> str:
    payload.messages.append(Messages(role=MessagesRole.USER, content=str(news)))

    resp = await giga.achat(payload)
    json = resp.choices[0].message.content

    payload.messages.pop()
    print(json)
    return json