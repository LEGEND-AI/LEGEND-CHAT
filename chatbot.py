from pyrogram import Client, filters
from pyrogram.types import *
from pymongo import MongoClient
import requests
import random
import os
import re
import asyncio
import time
from datetime import datetime
from googletrans import Translator
import emoji
LANG = os.environ.get("LANGUAGE", "hi")

ENV = bool(os.environ.get("ENV", False))

if ENV:
    from sample_config import Config  # noqa
elif os.path.exists("config.py"):
    from config import Development as Config  # noqa
    
bot = Client(
    "LegendBoy" ,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH ,
    bot_token = Config.BOT_TOKEN
)

BOT_NAME = Config.BOT_NAME
BOT_USERNAME = Config.BOT_USERNAME
MONGO_URL = Config.MONGO_URL

async def is_admins(chat_id: int):
    return [
        member.user.id
        async for member in bot.iter_chat_members(
            chat_id, filter="administrators"
        )
    ]




async def getTranslate(text, **kwargs):
    translator = Translator()
    result = None
    for _ in range(10):
        try:
            result = translator.translate(text, **kwargs)
        except Exception:
            translator = Translator()
            await sleep(0.1)
    return result


def soft_deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return emoji.get_emoji_regexp().sub("", inputString)

EMOJIOS = [ 
      "ð£",
      "ð¥",
      "ðª",
      "ð§¨",
      "â¡",
      "ð¤¡",
      "ð»",
      "ð",
      "ð©",
      "ð",
]
      

START = f"""
**à¹ Hey, I am [{Config.BOT_NAME}]({Config.START_IMG1})**
**â» á´É´ á´Éª-Êá´sá´á´ á´á´á´á´ á´É¢á´Êá´ á´Êá´á´Êá´á´.**
**ââââââââââââââââââ**
**â» á´sá´É¢á´ /chatbot [on/off]**
**à¹ á´á´ É¢á´á´ Êá´Êá´ á´sá´ /help**
"""

DEV_OP = [
    [
        InlineKeyboardButton(text="ð¥ Developer ð¥", url=f"https://t.me/LegendBoy_OP"),
        InlineKeyboardButton(text="â¨ Support â¨", url=f"https://t.me/LegendBot_OP"),
    ],
    [
        InlineKeyboardButton(
            text="ð§¸ Add me in your group ð§¸",
            url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="ð Helps & Cmds ð", callback_data="HELP"),
    ],
    [
        InlineKeyboardButton(text="âï¸ Source Code âï¸", url=f"https://github.com/LEGEND-AI/LEGEND-CHAT"),
        InlineKeyboardButton(text="âï¸ Updates âï¸", url=f"https://t.me/LegendBot_AI"),
    ],
]

PNG_BTN = [
    [
         InlineKeyboardButton(
             text="ð§¸ Add me Baby ð§¸",
             url=f"https://t.me/{Config.BOT_USERNAME}?startgroup=true",
         ),
     ],
     [
         InlineKeyboardButton(text="â¨ Support â¨", 
                              url=f"https://t.me/LegendBot_OP",
         ),
     ],
]


@bot.on_message(filters.command(["start", f"start@{Config.BOT_USERNAME}"]))
async def restart(client, m: Message):
    accha = await m.reply_text(
                text = random.choice(EMOJIOS),
    )
    await asyncio.sleep(1)
    await accha.edit("__á´Î¹Ð¸g á´ÏÐ¸g ê¨ï¸ ÑÑÎ±ÑÑÎ¹Ð¸g..__")
    await asyncio.sleep(0.2)
    await accha.edit("__á´Î¹Ð¸g á´ÏÐ¸g ê¨ï¸ sÑÎ±ÑÑÎ¹Ð¸g..__")
    await asyncio.sleep(0.2)
    await accha.delete()
    umm = await m.reply_sticker(
              sticker = Config.STKR,
    )
    await asyncio.sleep(2)
    await umm.delete()
    await m.reply_photo(
        photo = Config.START_IMG1,
        caption=f"""**à¹ Êá´Ê, Éª á´á´ [{Config.BOT_NAME}](t.me/{Config.BOT_USERNAME})**\n**â» á´É´ á´Éª-Êá´sá´á´ á´Êá´á´Êá´á´.**\n**ââââââââââââââââââ**\n**â» á´sá´É¢á´ /chatbot [on/off]**\n**à¹ á´á´ É¢á´á´ Êá´Êá´ á´sá´ /help**""",
        reply_markup=InlineKeyboardMarkup(DEV_OP),
    )
    
    
HELP_READ = "**á´sá´É¢á´ âï¸ï¸ï¸**\n**â» á´sá´** `/chatbot on` **á´á´ á´É´á´ÊÊá´ á´Êá´á´Êá´á´.**\n**â» á´sá´** `/chatbot off` **á´á´ á´Éªsá´ÊÊá´ á´Êá´ á´Êá´á´Êá´á´.**\n**à¹ É´á´á´á´ â» Êá´á´Ê á´Êá´ á´Êá´á´ á´ á´á´á´á´á´É´á´s Òá´Ê á´Êá´á´-Êá´á´ á´É´/á´ÒÒ á´¡á´Êá´ ÉªÉ´ É¢Êá´á´á´ á´É´ÊÊ!!**\n\n**â» á´sá´** `/ping` **á´á´ á´Êá´á´á´ á´Êá´ á´ÉªÉ´É¢ á´Ò á´Êá´ Êá´á´.**\n**Â© @LegendBoy_OP**"
HELP_BACK = [
     [
           InlineKeyboardButton(text="â¨ Back â¨", callback_data="HELP_BACK"),
     ],
]

@bot.on_callback_query()
async def cb_handler(Client, query: CallbackQuery):
    if query.data == "HELP":
     await query.message.edit_text(
                      text = HELP_READ,
                      reply_markup = InlineKeyboardMarkup(HELP_BACK),
     )
    elif query.data == "HELP_BACK":
            await query.message.edit(
                  text = START,
                  reply_markup=InlineKeyboardMarkup(DEV_OP),
        )
@bot.on_message(filters.command(["help", f"help@{Config.BOT_USERNAME}"], prefixes=["+", ".", "/", "-", "?", "$"]))
async def restart(client, message):
    hmm = await message.reply_text(
                        text = HELP_READ,
                        reply_markup= InlineKeyboardMarkup(HELP_BACK),
       )


@bot.on_message(filters.command(["ping","alive"], prefixes=["+", "/", "-", "?", "$", "&"]))
async def ping(client, message: Message):
        start = datetime.now()
        t = "__ÏÎ¹Ð¸gÎ¹Ð¸g...__"
        txxt = await message.reply(t)
        await asyncio.sleep(0.25)
        await txxt.edit_text("__ÏÎ¹Ð¸gÎ¹Ð¸g.....__")
        await asyncio.sleep(0.35)
        await txxt.delete()
        end = datetime.now()
        ms = (end-start).microseconds / 1000
        await message.reply_photo(
                             photo=Config.START_IMG1,
                             caption=f"Ð½ey Ð²Î±Ð²Ñ!!\n**[{Config.BOT_NAME}](t.me/{Config.BOT_USERNAME})** Î¹Ñ alÎ¹ve ð¥ Î±nd worÄ¸Î¹ng ÒÎ¹ne wÎ¹ÑÐ½ a pÎ¹ng oÒ\nâ¥ `{ms}` ms\n\n**Ð¼Î±dÑ ÏÎ¹ÑÐ½ â£ï¸ Ð²Ñ [LegendBoy](https://t.me/LegendBoy_OP)**",
                             reply_markup=InlineKeyboardMarkup(PNG_BTN),
       )

@bot.on_message(
    filters.command(["chatbot off", f"chatbot@{BOT_USERNAME} off"], prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def chatbotofd(client, message):
    legenddb = MongoClient(MONGO_URL)    
    legend = legenddb["LegendDb"]["Legend"]     
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
           await is_admins(chat_id)
        ):
           return await message.reply_text(
                "Sorry Sir, You are not admin"
            )
    is_legend = legend.find_one({"chat_id": message.chat.id})
    if not is_legend:
        legend.insert_one({"chat_id": message.chat.id})
        await message.reply_text(f"Chatbot Disabled!")
    if is_legend:
        await message.reply_text(f"ChatBot Already Disabled")
    

@bot.on_message(
    filters.command(["chatbot on", f"chatbot@{BOT_USERNAME} on"] ,prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def chatboton(client, message):
    legenddb = MongoClient(MONGO_URL)    
    legend = legenddb["LegendDb"]["Legend"]     
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
            await is_admins(chat_id)
        ):
            return await message.reply_text(
                "You are not admin"
            )
    is_legend = legend.find_one({"chat_id": message.chat.id})
    if not is_legend:           
        await message.reply_text(f"Chatbot Already Enabled")
    if is_legend:
        legend.delete_one({"chat_id": message.chat.id})
        await message.reply_text(f"ChatBot Enabled!")
    

@bot.on_message(
    filters.command(["chatbot", f"chatbot@{BOT_USERNAME}"], prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def chatbot(client, message):
    await message.reply_text(f"**á´sá´É¢á´:**\n/**chatbot [on/off]**\n**á´Êá´á´-Êá´á´ á´á´á´á´á´É´á´(s) á´¡á´Êá´ ÉªÉ´ É¢Êá´á´á´ á´É´ÊÊ!**")


@bot.on_message(
 (
        filters.text
        | filters.sticker
    )
    & ~filters.private
    & ~filters.bot,
)
async def legendai(client: Client, message: Message):

   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"]   

   if not message.reply_to_message:
       legenddb = MongoClient(MONGO_URL)
       legend = legenddb["LegendDb"]["Legend"] 
       is_legend = legend.find_one({"chat_id": message.chat.id})
       if not is_legend:
           await bot.send_chat_action(message.chat.id, "typing")
           K = []  
           is_chat = chatai.find({"word": message.text})  
           k = chatai.find_one({"word": message.text})      
           if k:               
               for x in is_chat:
                   K.append(x['text'])          
               hey = random.choice(K)
               is_text = chatai.find_one({"text": hey})
               Yo = is_text['check']
               if Yo == "sticker":
                   await message.reply_sticker(f"{hey}")
               if not Yo == "sticker":
                   text = soft_deEmojify(hey.strip())
                   lan = LANG
                   lan = lan.strip()
                   translated = await getTranslate(text, dest=lan)
                   after_tr_text = translated.text
                   betu = f"{hey} {after_tr_text}"
                   llol = [x for x in betu.split()]
                   IPIC = random.choice(llol)
                   await message.reply_text(f"{IPIC}")
   if message.reply_to_message:  
       legenddb = MongoClient(MONGO_URL)
       legend = legenddb["LegendDb"]["Legend"] 
       is_legend = legend.find_one({"chat_id": message.chat.id})    
       getme = await bot.get_me()
       bot_id = getme.id                             
       if message.reply_to_message.from_user.id == bot_id: 
           if not is_legend:                   
               await bot.send_chat_action(message.chat.id, "typing")
               K = []  
               is_chat = chatai.find({"word": message.text})
               k = chatai.find_one({"word": message.text})      
               if k:       
                   for x in is_chat:
                       K.append(x['text'])
                   hey = random.choice(K)
                   is_text = chatai.find_one({"text": hey})
                   Yo = is_text['check']
                   if Yo == "sticker":
                       await message.reply_sticker(f"{hey}")
                   if not Yo == "sticker":
                       text = soft_deEmojify(hey.strip())
                       lan = LANG
                       lan = lan.strip()
                       translated = await getTranslate(text, dest=lan)
                       after_tr_text = translated.text
                       betu = f"{hey} {after_tr_text}"
                       llol = [x for x in betu.split()]
                       IPIC = random.choice(llol)
                       await message.reply_text(f"{IPIC}")
       if not message.reply_to_message.from_user.id == bot_id:          
           if message.sticker:
               is_chat = chatai.find_one({"word": message.reply_to_message.text, "id": message.sticker.file_unique_id})
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.text, "text": message.sticker.file_id, "check": "sticker", "id": message.sticker.file_unique_id})
           if message.text:                 
               is_chat = chatai.find_one({"word": message.reply_to_message.text, "text": message.text})                 
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.text, "text": message.text, "check": "none"})    
               

@bot.on_message(
 (
        filters.sticker
        | filters.text
    )
    & ~filters.private
    & ~filters.bot,
)
async def legendstickerai(client: Client, message: Message):

   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"]   

   if not message.reply_to_message:
       legenddb = MongoClient(MONGO_URL)
       legend = legenddb["LegendDb"]["Legend"] 
       is_legend = legend.find_one({"chat_id": message.chat.id})
       if not is_legend:
           await bot.send_chat_action(message.chat.id, "typing")
           K = []  
           is_chat = chatai.find({"word": message.sticker.file_unique_id})      
           k = chatai.find_one({"word": message.text})      
           if k:           
               for x in is_chat:
                   K.append(x['text'])
               hey = random.choice(K)
               is_text = chatai.find_one({"text": hey})
               Yo = is_text['check']
               if Yo == "text":
                   text = soft_deEmojify(hey.strip())
                   lan = LANG
                   lan = lan.strip()
                   translated = await getTranslate(text, dest=lan)
                   after_tr_text = translated.text
                   betu = f"{hey} {after_tr_text}"
                   llol = [x for x in betu.split()]
                   IPIC = random.choice(llol)
                   await message.reply_text(f"{IPIC}")
               if not Yo == "text":
                   await message.reply_sticker(f"{hey}")
   
   if message.reply_to_message:
       agoradb = MongoClient(MONGO_URL)
       legend = legenddb["LegendDb"]["Legend"] 
       is_legend = legend.find_one({"chat_id": message.chat.id})
       getme = await bot.get_me()
       bot_id = getme.id
       if message.reply_to_message.from_user.id == bot_id: 
           if not is_legend:                    
               await bot.send_chat_action(message.chat.id, "typing")
               K = []  
               is_chat = chatai.find({"word": message.text})
               k = chatai.find_one({"word": message.text})      
               if k:           
                   for x in is_chat:
                       K.append(x['text'])
                   hey = random.choice(K)
                   is_text = chatai.find_one({"text": hey})
                   Yo = is_text['check']
                   if Yo == "text":
                       text = soft_deEmojify(hey.strip())
                       lan = LANG
                       lan = lan.strip()
                       translated = await getTranslate(text, dest=lan)
                       after_tr_text = translated.text
                       betu = f"{hey} {after_tr_text}"
                       llol = [x for x in betu.split()]
                       IPIC = random.choice(llol)
                       await message.reply_text(f"{IPIC}")
                   if not Yo == "text":
                       await message.reply_sticker(f"{hey}")
       if not message.reply_to_message.from_user.id == bot_id:          
           if message.text:
               is_chat = chatai.find_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.text})
               if not is_chat:
                   toggle.insert_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.text, "check": "text"})
           if message.sticker:                 
               is_chat = chatai.find_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.sticker.file_id})                 
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.sticker.file_id, "check": "none"})    
               


@bot.on_message(
    (
        filters.text
        | filters.sticker
    )
    & filters.private
    & ~filters.bot,
)
async def vickprivate(client: Client, message: Message):

   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"]
   if not message.reply_to_message: 
       await bot.send_chat_action(message.chat.id, "typing")
       K = []  
       is_chat = chatai.find({"word": message.text})                 
       for x in is_chat:
           K.append(x['text'])
       hey = random.choice(K)
       is_text = chatai.find_one({"text": hey})
       Yo = is_text['check']
       if Yo == "sticker":
           await message.reply_sticker(f"{hey}")
       if not Yo == "sticker":
           text = soft_deEmojify(hey.strip())
           lan = LANG
           lan = lan.strip()
           translated = await getTranslate(text, dest=lan)
           after_tr_text = translated.text
           betu = f"{hey} {after_tr_text}"
           llol = [x for x in betu.split()]
           IPIC = random.choice(llol)
           await message.reply_text(f"{IPIC}")
   if message.reply_to_message:            
       getme = await bot.get_me()
       bot_id = getme.id       
       if message.reply_to_message.from_user.id == bot_id:                    
           await bot.send_chat_action(message.chat.id, "typing")
           K = []  
           is_chat = chatai.find({"word": message.text})                 
           for x in is_chat:
               K.append(x['text'])
           hey = random.choice(K)
           is_text = chatai.find_one({"text": hey})
           Yo = is_text['check']
           if Yo == "sticker":
               await message.reply_sticker(f"{hey}")
           if not Yo == "sticker":
               text = soft_deEmojify(hey.strip())
               lan = LANG
               lan = lan.strip()
               translated = await getTranslate(text, dest=lan)
               after_tr_text = translated.text
               betu = f"{hey} {after_tr_text}"
               llol = [x for x in betu.split()]
               IPIC = random.choice(llol)
               await message.reply_text(f"{IPIC}")
       

@bot.on_message(
 (
        filters.sticker
        | filters.text
    )
    & filters.private
    & ~filters.bot,
)
async def vickprivatesticker(client: Client, message: Message):

   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"] 
   if not message.reply_to_message:
       await bot.send_chat_action(message.chat.id, "typing")
       K = []  
       is_chat = chatai.find({"word": message.sticker.file_unique_id})                 
       for x in is_chat:
           K.append(x['text'])
       hey = random.choice(K)
       is_text = chatai.find_one({"text": hey})
       Yo = is_text['check']
       if Yo == "text":
           text = soft_deEmojify(hey.strip())
           lan = LANG
           lan = lan.strip()
           translated = await getTranslate(text, dest=lan)
           after_tr_text = translated.text
           betu = f"{hey} {after_tr_text}"
           llol = [x for x in betu.split()]
           IPIC = random.choice(llol)
           await message.reply_text(f"{IPIC}")
       if not Yo == "text":
           await message.reply_sticker(f"{hey}")
   if message.reply_to_message:            
       getme = await bot.get_me()
       bot_id = getme.id       
       if message.reply_to_message.from_user.id == bot_id:                    
           await bot.send_chat_action(message.chat.id, "typing")
           K = []  
           is_chat = chatai.find({"word": message.sticker.file_unique_id})                 
           for x in is_chat:
               K.append(x['text'])
           hey = random.choice(K)
           is_text = chatai.find_one({"text": hey})
           Yo = is_text['check']
           if Yo == "text":
              text = soft_deEmojify(hey.strip())
              lan = LANG
              lan = lan.strip()
              translated = await getTranslate(text, dest=lan)
              after_tr_text = translated.text
              betu = f"{hey} {after_tr_text}"
              llol = [x for x in betu.split()]
              IPIC = random.choice(llol)
              await message.reply_text(f"{IPIC}")
           if not Yo == "text":
               await message.reply_sticker(f"{hey}")

print(f"{BOT_NAME} Éªs á´ÊÉªá´ á´!")
print("----------------")
print("Starting Bot Mode!")
print("â Legend Chat Bot Has Been Deployed Successfully â")
print("OWNER - @LegendBoy_OP")
print("Group - @LegendBot_XDS")
print("----------------")
bot.run()
