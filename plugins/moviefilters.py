from Script import script
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

@Client.on_message(filters.regex("hi"))
async def regex(bot, msg):
    buttons = [[
        InlineKeyboardButton("ᴅɪᴅɴ'ᴛ ɢᴇᴛ ᴍᴏᴠɪᴇ", url='t.me/moviesupdateck')       
        ],[
        InlineKeyboardButton("ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ", url='t.me/cinemakodathi')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await msg.reply_photo(
        photo="https://telegra.ph/file/028b840597616b48ac356.jpg",
        caption=script.UPDATE_CMD.format(msg.from_user.mention),
        reply_markup=reply_markup,
        parse_mode="html")
