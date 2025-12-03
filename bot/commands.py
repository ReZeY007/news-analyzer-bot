from aiogram.types.bot_command import BotCommand

start_command = BotCommand(command='start', description='Start bot')
findnews_command = BotCommand(command='findnews', description='Find news by topic')

commands = [start_command, findnews_command]