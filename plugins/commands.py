from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters

HOME_TEXT = "👋🏻 **Hi [{}](tg://user?id={})**,\nI'm JD \nഎനിക്ക് ഗ്രൂപ്പിലും ചാനലിലും പാട്ടു പാടാൻ പാട്ടും 😌 . I Can Play Radio/Stream Music In Channels & Groups 24x7 Nonstop. Made with ❤️ By @akhilbaiju!"
HELP = """

Life is very short Nanba
     Always be happy 😉


"""

@Client.on_message(filters.command('start'))
async def start(client, message):
    buttons = [
        [
        InlineKeyboardButton('Channel', url='https://t.me/honeybeemovies'),
        InlineKeyboardButton('Youtube', url='https://www.youtube.com/channel/UCe5RaLkqRimYwdWss4FpH2w'),
    ],
    [
        InlineKeyboardButton('😎 My Father 😎', url='https://t.me/akhilbaiju'),
    ],
    [
        InlineKeyboardButton('⚙️ Help ⚙️', callback_data='help'),
        
    ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply(HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)

@Client.on_message(filters.command("help"))
async def show_help(client, message):
    await message.reply_text(HELP)
