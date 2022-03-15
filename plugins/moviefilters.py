from Script import script
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Client.on_message(filters.regex("FAST AND FURIOUS") | filters.regex("Fast And Furious") | filters.regex("fast and furious"))
async def regex(bot, msg):
    buttons = [[
        InlineKeyboardButton("Fast and furious", callback_data="tip2")
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

@Client.on_message(filters.regex("HOME ALONE") | filters.regex("home alone") | filters.regex("Home Alone"))
async def home(bot, msg):
    buttons = [[
        InlineKeyboardButton("🏠 HOME ALONE 🏠", callback_data="tip2")
        ],[      
        InlineKeyboardButton("HM 1", callback_data="f2001"),
        InlineKeyboardButton("HM 2", callback_data="f2003"),
        InlineKeyboardButton("HM 3", callback_data="f2006")
        ],[
        InlineKeyboardButton("HM 4", callback_data="f2009"),
        InlineKeyboardButton("HM 5", callback_data="f2011"),
        InlineKeyboardButton("HM 6", callback_data="f2013"),
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await msg.reply_photo(
        photo="https://telegra.ph/file/8beaabbd30f4dbf084f4e.jpg",
        caption=script.HOME_ALONE.format(msg.from_user.mention),
        reply_markup=reply_markup,
        parse_mode="html")
  
@Client.on_message(filters.regex("MAHAAN") | filters.regex("mahaan") | filters.regex("Mahaan"))
async def mahaan(bot, msg):
    buttons = [[
        InlineKeyboardButton("🦋 MAHAAN MALAYALAM 🦋", url="https://t.me/lisamoviebot?start=DSTORE-NDFfNDRfLTEwMDE2NTc2MjkyODVfL2JhdGNo")
        ],[
        InlineKeyboardButton("TAMIL", url="https://t.me/lisamoviebot?start=DSTORE-NDVfNDhfLTEwMDE2NTc2MjkyODVfL2JhdGNo")
        ],[
        InlineKeyboardButton("‼️ ALERT ‼️", callback_data="alert")
        ],[
        InlineKeyboardButton("🌀 Jᴏɪɴ ᴄʜᴀɴɴᴇL 🌀", url="https://t.me/moviesupdateck")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await msg.reply_sticker(
        sticker="CAACAgUAAxkBAAECGahiL6CDY53FYO4iRYXbu_ZXmtHvzAACLAUAAvv_KFQWafOBgNotdR4E",
        reply_markup=reply_markup
    )
@Client.on_message(filters.regex("JAN E MAN") | filters.regex("jan e man") | filters.regex("Jan e man") | filters.regex("Jan E Man"))
async def regex(bot, msg):
    buttons = [[
        InlineKeyboardButton("🔘 JAN E MAN 🔘", url="https://t.me/lisamoviebot?start=DSTORE-NDlfNTNfLTEwMDE2NTc2MjkyODVfL2JhdGNo")
        ],[
        InlineKeyboardButton("‼️ ALERT ‼️", callback_data="art")
        ],[
        InlineKeyboardButton("🌀 Jᴏɪɴ ᴄʜᴀɴɴᴇL 🌀", url="https://t.me/moviesupdateck")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await msg.reply_sticker(
        sticker="CAACAgUAAxkBAAECGbViL-s5MJSgV4DmpZ0xG83RKZbdowAC2gQAAi5HqVR7BrHkcRQZ4B4E",
        reply_markup=reply_markup
    )
