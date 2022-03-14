from Script import script
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Client.on_message(filters.regex("FAST AND FURIOUS") | filters.regex("Fast And Furious") | filters.regex("fast and furious"))
async def regex(bot, msg):
    buttons = [[
        InlineKeyboardButton("Fast and furious", callback_data="ftfuri")
        ],[      
        InlineKeyboardButton("2001", callback_data="f2001"),
        InlineKeyboardButton("2003", callback_data="f2003"),
        InlineKeyboardButton("2006", callback_data="f2006"),
        InlineKeyboardButton("2009", callback_data="f2009")
        ],[
        InlineKeyboardButton("2011", callback_data="f2011"),
        InlineKeyboardButton("2013", callback_data="f2013"),
        InlineKeyboardButton("2015", callback_data="f2015"),
        InlineKeyboardButton("2017", callback_data="f2017")
        ],[
        InlineKeyboardButton("Fast And Furious Presents: Hobbs and Shaw", callback_data="f2019")
        ],[
        InlineKeyboardButton("F9 The Fast Saga", callback_data="f2021")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await msg.reply_photo(
        photo="https://telegra.ph/file/8f74216a74c06f881a670.jpg",
        caption=script.FAST_FURI.format(msg.from_user.mention),
        reply_markup=reply_markup,
        parse_mode="html")


