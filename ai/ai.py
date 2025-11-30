from os import getenv
from gigachat import GigaChat
from gigachat.models import Messages, MessagesRole
import asyncio


giga = GigaChat(credentials=getenv('GIGACHAT_KEY'),
                verify_ssl_certs=False,
                model='GigaChat-2',
                )

system_prompt = 'Ты бот-анализатор новостей. Твоя задача проанализировать общий эмоциональный окрас новостей, выделить ключевые слова и написать краткую сводку.'
messages = [Messages(role=MessagesRole.SYSTEM, content=system_prompt)]


async def ai_request(message):
    resp = await asyncio.to_thread(giga.chat, message)
    answer = resp.choices[0].message.content
    
    return answer