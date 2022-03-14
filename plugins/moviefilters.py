from Script import script
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

@Client.on_message(filters.regex("hi"))
async def regex(bot, msg):
    buttons = [[
        InlineKeyboardButton("Fast and furious", callback_data="ftfuri")
        ],[      
        InlineKeyboardButton("2001", callback_data="f2001"),
        InlineKeyboardButton("2003", callback_data="ftfuri"),
        InlineKeyboardButton("2006", callback_data="ftfuri"),
        InlineKeyboardButton("2009", callback_data="ftfuri")
        ],[
        InlineKeyboardButton("2011", callback_data="ftfuri"),
        InlineKeyboardButton("2013", callback_data="ftfuri"),
        InlineKeyboardButton("2015", callback_data="ftfuri"),
        InlineKeyboardButton("2017", callback_data="ftfuri")
        ],[
        InlineKeyboardButton("Fast And Furious Presents: Hobbs and Shaw", callback_data="ftfuri")
        ],[
        InlineKeyboardButton("F9 The Fast Saga", callback_data="ftfuri")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await msg.reply_photo(
        photo="https://telegra.ph/file/8f74216a74c06f881a670.jpg",
        caption=script.FAST_FURI.format(msg.from_user.mention),
        reply_markup=reply_markup,
        parse_mode="html")


@farshad.on_callback_query()
async def callback(bot, msg: CallbackQuery):
    if msg.data == "f2001":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-N185Xy0xMDAxNjU3NjI5Mjg1Xy9iYXRjaA")                     
        ]]
        await msg.reply_photo(
            photo="https://telegra.ph/file/a19c66ea096312b05e2ba.jpg",
            caption="🎬 Title: Fast & Furious 1/n📅 Year: 2001/n🎙️Language: English/n📊Rating: 6.8/10"),
            reply_markup=reply_markup,
            parse_mode='html'


