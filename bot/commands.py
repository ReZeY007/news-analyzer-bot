from aiogram.types.bot_command import BotCommand

start_command = BotCommand(command='start', description='Start bot')
findnews_command = BotCommand(command='findnews', description='Find news by topic')
analyzenews_command = BotCommand(command='analyzenews', description='Analyze news by topic')

savetopic_command = BotCommand(command='savetopic', description='Save topic to use it later')
deletetopic_command = BotCommand(command='deletetopic', description='Delete topic from saved')

commands = [start_command, findnews_command, analyzenews_command, savetopic_command, deletetopic_command]