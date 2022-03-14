from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

@Client.on_message(filters.regex("hello"))
async def regex(bot, msg):
    buttons = [[
        InlineKeyboardButton("ᴅɪᴅɴ'ᴛ ɢᴇᴛ ᴍᴏᴠɪᴇ", url='t.me/moviesupdateck')       
        ],[
        InlineKeyboardButton("ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ", url='t.me/cinemakodathi')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_photo(
        photo="https://telegra.ph/file/028b840597616b48ac356.jpg",
        caption=script.UPDATE_CMD.format(message.from_user.mention),
        reply_markup=reply_markup,
        parse_mode="html")

#await msg.reply_text("hello bro")
