from config import *
import os
import sys
api_id = API_ID
api_hash = API_HASH

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += f'{ele}\n'
    return str1

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

from db import BotDB
bd = BotDB('bot_data.sqlite')

from telethon import TelegramClient, events

client = TelegramClient('anon', api_id, api_hash)

'''
@client.on(events.NewMessage)
async def my_event_handler(event):
    if 'hello' in event.raw_text:
        await event.reply('hi!')
'''
@client.on(events.NewMessage(pattern=r'\.save'))
async def handler(event):
    if event.is_reply:
        replied = await event.get_reply_message()
        sender = replied.sender
        await client.download_profile_photo(sender)
        await event.respond('Saved your photo {}'.format(sender.username))

@client.on(events.NewMessage(outgoing=True, pattern=r'(?i).*/добавить канал:'))
async def handler(event):
    channel = event.message.message.split(':')[1].strip()
    last_m = await client.get_messages(channel)
    
    if not last_m:
        await event.respond('Канал не найден')
    else:
        if bd.channels_exist(channel):
            await event.respond('Такой канал уже добавлен')
        else:
            bd.add_channel_to_repost(channel)
            await event.respond('Канал добавлен')
            os.execv(sys.executable, [sys.executable] + sys.argv)

@client.on(events.NewMessage(outgoing=True, pattern=r'(?i).*/удалить канал:'))
async def handler(event):
    channel = event.message.message.split(':')[1].strip()
    if bd.channels_exist(channel):
        bd.remove_channel_to_repost(channel)
        await event.respond(f'Канал "{channel}" удалён')
    else:
        await event.respond('Канал не найден')

@client.on(events.NewMessage(outgoing=True, pattern=r'(?i).*/изменить канал для получения:'))
async def handler(event):
    channel = event.message.message.split(':')[1].strip()
    last_m = '1'
    if not last_m:
        await event.respond('Канал не найден или пуст')
    else:
        bd.set_channel_to_repost(channel)
        await event.respond('Канал добавлен')
        os.execv(sys.executable, [sys.executable] + sys.argv)

@client.on(events.NewMessage(outgoing=True, pattern=r'(?i).*/изменить чат для получения:'))
async def handler(event):
    chat = event.message.message.split(':')[1].strip()
    last_m = '1'
    if not last_m:
        await event.respond('Чат не найден или пуст')
    else:
        bd.set_chat_to_repost(chat)
        await event.respond('Чат изменён')
        os.execv(sys.executable, [sys.executable] + sys.argv)


@client.on(events.NewMessage(pattern='/info'))
async def handler(event):
    await event.respond(f'{INFO}')  
@client.on(events.NewMessage(pattern='/start'))
async def handler(event):
    await event.respond(f'{START}')

@client.on(events.NewMessage(pattern='/узать id'))
async def handler(event):
    chats = []
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'имеет ID', dialog.id)
        chats.append(f'`{dialog.name}` имеет ID `{dialog.id}`')
    print(listToString(chats))
    await event.respond(listToString(chats))

@client.on(events.NewMessage(pattern='/список каналов'))
async def handler(event):
    await event.respond(f'Список каналов: {bd.get_channels()}')

@client.on(events.NewMessage(pattern='/канал для получения'))
async def handler(event):
    await event.respond(f'{bd.get_channel_to_repost()}')

@client.on(events.NewMessage(pattern='/чат для получения'))
async def handler(event):
    await event.respond(f'{bd.get_chat_to_repost()}')

@client.on(events.NewMessage(bd.get_channels()))
async def handler(event):
    chat_to_repost = int(bd.get_chat_to_repost())
    channel_to_repost = int(bd.get_channel_to_repost())
    if channel_to_repost != '1':
        try: 
            await client.forward_messages(channel_to_repost, event.message)
        except:
            await event.respond(f'Произошла ошибка')
    if chat_to_repost != '0':
        try: 
            await client.forward_messages(chat_to_repost, event.message)
        except:
            await event.respond(f'Произошла ошибка')


client.start()
client.run_until_disconnected()