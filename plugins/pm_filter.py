# Kanged From @TroJanZheX
import asyncio
import re
import ast

from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import ADMINS, AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, P_TTI_SHOW_OFF, IMDB, \
    SINGLE_BUTTON, SPELL_CHECK_REPLY, IMDB_TEMPLATE, CH_FILTER, CH_LINK
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}

NORGE_IMG = f"https://telegra.ph/file/1616bc34ec34c9d74b5d2.jpg"

IMDB_TEMPLATE = """<b>🏷 Title</b>: <a href={url}>{title}</a>
🎭 Genres: {genres}
📆 Year: <a href={url}/releaseinfo>{year}</a>
🌟 Rating: <a href={url}/ratings>{rating}</a> / 10 (based on {votes} user ratings.)
☀️ Languages : <code>{languages}</code>
📀 RunTime: {runtime} Minutes
📆 Release Info : {release_date}
"""

@Client.on_message(filters.group & filters.text & ~filters.edited & filters.incoming)
async def give_filter(client, message):
    k = await manual_filters(client, message)
    if k == False:
        await auto_filter(client, message)


@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer("oKda", show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.", show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    settings = await get_settings(query.message.chat.id)
    if settings['button']:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"📂{get_size(file.file_size)} 📂{file.file_name}", callback_data=f'files#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}", callback_data=f'files#{file.file_id}'
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'files_#{file.file_id}',
                ),
            ]
            for file in files
        ]

    if 0 < offset <= 10:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 10
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⏪ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
             InlineKeyboardButton(f"📃 Pages {round(int(offset) / 10) + 1} / {round(total / 10)}",
                                  callback_data="pages")]
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"🗓 {round(int(offset) / 10) + 1} / {round(total / 10)}", callback_data="pages"),
             InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("⏪ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"🗓 {round(int(offset) / 10) + 1} / {round(total / 10)}", callback_data="pages"),
                InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{req}_{key}_{n_offset}")
            ],
        )
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()


@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("okDa", show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.message_id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Checking for Movie in database...')
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else:
            k = await query.message.edit('This Movie Not Found In DataBase')
            await asyncio.sleep(10)
            await k.delete()


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.edit(
            text="<b>Cʟᴏꜱɪɴɢ</b>"
        )
        await query.message.edit(
            text="<b>Cʟᴏꜱɪɴɢ</b>⭗ ⭗ ⭗ ⭗ ⭗ ⭗"
        )
        await query.message.edit(
            text="<b>Cʟᴏꜱɪɴɢ ɪɴ ᴘʀᴏɢʀᴇꜱꜱ</b>⦿ ⦿ ⦿ ⭗ ⭗ ⭗"
        )
        await query.message.edit(
            text="<b>Cʟᴏꜱɪɴɢ ɪɴ ᴘʀᴏɢʀᴇꜱꜱ</b>⦿ ⦿ ⦿ ⦿ ⭗ ⭗"
        )
        await query.message.edit(
            text="<b>Cʟᴏꜱɪɴɢ 𝙸𝙽 𝙿𝚁𝙾𝙶𝚁𝙴𝚂𝚂</b>⦿ ⦿ ⦿ ⦿ ⦿ ⭗"
        )
        await query.message.edit(
            text="<b>Cʟᴏꜱɪɴɢ ɪɴ ᴘʀᴏɢʀᴇꜱꜱ</b>⦿ ⦿ ⦿ ⦿ ⦿ ⦿"
        )
        await query.message.delete()
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return await query.answer('Piracy Is Crime')
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return await query.answer('Piracy Is Crime')

        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return await query.answer('Piracy Is Crime')

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == "creator") or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == "creator") or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("That's not for you!!", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode="md"
        )
        return await query.answer('Piracy Is Crime')
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text('Some error occurred!!', parse_mode="md")
        return await query.answer('Piracy Is Crime')
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode="md"
            )
        return await query.answer('Piracy Is Crime')
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode="md"
            )
        return await query.answer('Piracy Is Crime')
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return await query.answer('Piracy Is Crime')
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    if query.data.startswith("file"):
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        type = files.file_type
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)

                buttons = [[
                  InlineKeyboardButton('JOIN GROUP', url='https://t.me/cinemakodathi')
                  ]]                                        
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"

        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            elif settings['botpm']:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            else:
                ms = await client.send_cached_media(
                    chat_id=CH_FILTER,
                    file_id=file_id,
                    caption=f_caption,
                    protect_content=True if ident == "filep" else False 
                )
                msg1 = await query.message.reply(
                f'<b>Hey 👋{query.from_user.mention}\n\n'
                f'<b>📫 Yᴏʀ Fɪʟᴇ ɪꜱ Rᴇᴀᴅʏ 👇\n\n'
                f'<b>🎬 Mᴏᴠɪᴇ Nᴀᴍᴇ: {title}</b>\n\n'
                f'<b>⚙️ Mᴏᴠɪᴇ Sɪᴢᴇ: {size}</b>\n\n'
                f'<b>📂 Mᴏᴠɪᴇ Tʏᴘᴇ: {type}</b>\n\n'
                '<code>THis file will be deleted in 5 minutes.!</code>',
                True,
                'html',
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔰𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃 𝐍𝐎𝐖🔰", url = ms.link)
                        ],
                        [
                            InlineKeyboardButton("⚠️ 𝐂𝐚𝐧'𝐭 𝐀𝐜𝐜𝐞𝐬𝐬❓𝐂𝐥𝐢𝐜𝐤 𝐇𝐞𝐫𝐞 ⚠️", url = f"{CH_LINK}")
                        ]
                    ]
                )
            )
            await query.answer('Check Out The Chat',show_alert=True)
            await asyncio.sleep(1000)
            await msg1.delete()
            await msg.delete()
            del msg1, msg
        except Exception as e:
            logger.exception(e, exc_info=True)
            await query.answer(f"Encountering Issues", True)

    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒", show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
                buttons = [[
                  InlineKeyboardButton('JOIN GROUP', url='https://t.me/cinemakodathi')
                  ]]
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        await query.answer()
        ms = await client.send_cached_media(
            chat_id=CH_FILTER,
            file_id=file_id,
            caption=f_caption,
            protect_content=True if ident == 'checksubp' else False
        )
    elif query.data == "tip2": 
        await query.answer(f" • ബ്രോ ഇതിലല്ല 😃 \n\n • താഴെ വരുന്ന മൂവി ലിസ്റ്റിലാണ് ഞെക്കേണ്ടത്😁",show_alert=True)
    elif query.data == "sub": 
        await query.answer(f" • ബ്രോ ഇതിലല്ല 😃 \n\n • ഗ്രൂപ്പിൽ വരുന്ന മൂവി ലിസ്റ്റിലാണ് ഞെക്കേണ്ടത്😁",show_alert=True)
    elif query.data == "imd_alert":
        imdb = await get_poster(query.message.reply_to_message.text)
        await query.answer(f"""🏷 Title: {imdb['title']} 
🎭 Genres: {imdb['genres']} 
📆 Year: {imdb['year']} 
🌟 Rating: {imdb['rating']} 
☀️ Languages : {imdb['languages']} 
📀 RunTime: {imdb['runtime']} Minutes
📆 Release Info : {imdb['release_date']} 
""",show_alert=True)


    
#boutton new add akkiye
    elif query.data == "pages":
        await query.answer()
    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton('ᴄʟɪᴄᴋ ʜᴇʀᴇ', callback_data="mfk1"),
            InlineKeyboardButton('ꜱᴇᴀʀᴄʜ ᴍᴏᴠɪᴇꜱ', callback_data="mfk2") 
            ],[
            InlineKeyboardButton('ᴀᴅᴍɪɴ', url="https://t.me/farshadck")                    
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "mfk1":
        buttons = [[
            InlineKeyboardButton('ʟᴀᴛᴇꜱᴛ ᴍᴏᴠɪᴇꜱ', callback_data="moviekittan"),
            InlineKeyboardButton('ᴀʙᴏᴜᴛ & ʜᴇʟᴩ', callback_data='stats')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MFK_1.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode='html'
        )

    elif query.data == "f2001":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-N185Xy0xMDAxNjU3NjI5Mjg1Xy9iYXRjaA")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/a19c66ea096312b05e2ba.jpg",
            caption="🎬 Title: Fast & Furious 1/n📅 Year: 2001/n🎙️Language: English/n📊Rating: 6.8/10",
            reply_markup=reply_markup,
            parse_mode='html'
        
        )  

    elif query.data == "f2003":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-MTBfMTJfLTEwMDE2NTc2MjkyODVfL2JhdGNo")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/3f495cd7b84543089e2cc.jpg",
            caption="🎬 Title: 2 Fast 2 Furious 1/n📅 Year: 2003/n🎙️Language: English/n📊Rating: 6.8/10",
            reply_markup=reply_markup,
            parse_mode='html'
        
        )
    elif query.data == "f2006":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-MTNfMTZfLTEwMDE2NTc2MjkyODVfL2JhdGNo")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/c7b97d902e0b94dbfd50a.jpg",
            caption="🎬 Title: Fast & Furious 3/n📅 Year: 2006/n🎙️Language: English/n📊Rating: 6.8/10",
            reply_markup=reply_markup,
            parse_mode='html'
        
        )
    elif query.data == "f2009":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-MTdfMTlfLTEwMDE2NTc2MjkyODVfL2JhdGNo")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/cb6f3644a2223a33c1df5.jpg",
            caption="🎬 Title: Fast & Furious 4/n📅 Year: 2009/n🎙️Language: English/n📊Rating: 6.8/10",
            reply_markup=reply_markup,
            parse_mode='html'
        
        )
    elif query.data == "f2011":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-MjBfMjJfLTEwMDE2NTc2MjkyODVfL2JhdGNo")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/d8cc66612de7d1d0ed4d3.jpg",
            caption="🎬 Title: Fast & Furious 5/n📅 Year: 2011/n🎙️Language: English/n📊Rating: 6.8/10",
            reply_markup=reply_markup,
            parse_mode='html'
        
        )
    elif query.data == "f2013":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-MjNfMjVfLTEwMDE2NTc2MjkyODVfL2JhdGNo")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/7fcde6e1c720a8a34ea83.jpg",
            caption="🎬 Title: Fast & Furious 6/n📅 Year: 2013/n🎙️Language: English/n📊Rating: 6.8/10",
            reply_markup=reply_markup,
            parse_mode='html'
        
        )
    elif query.data == "f2015":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-MjZfMjhfLTEwMDE2NTc2MjkyODVfL2JhdGNo")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/c3ea555fca167431cec36.jpg",
            caption="🎬 Title: Fast & Furious 7/n📅 Year: 2015/n🎙️Language: English/n📊Rating: 6.8/10",
            reply_markup=reply_markup,
            parse_mode='html'
        
        )
    elif query.data == "f2017":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-MjlfMzFfLTEwMDE2NTc2MjkyODVfL2JhdGNo")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/8450380165caa3b01c5cf.jpg",
            caption="🎬 Title: Fast & Furious 8/n📅 Year: 2017/n🎙️Language: English/n📊Rating: 6.8/10",
            reply_markup=reply_markup,
            parse_mode='html'
        
        )
    elif query.data == "f2019":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-MzJfMzRfLTEwMDE2NTc2MjkyODVfL2JhdGNo")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/8da4cfb40e535acf85055.jpg",
            caption="🎬 Title: ast & Furious Presents: Hobbs & Shaw 3/n📅 Year: 2019/n🎙️Language: English/n📊Rating: 6.8/10",
            reply_markup=reply_markup,
            parse_mode='html'
        
        )
    elif query.data == "f2021":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-MzVfNDBfLTEwMDE2NTc2MjkyODVfL2JhdGNo")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/8affe4898f81c38849fc5.jpg",
            caption="🎬 Title: Fast & Furious 9/n📅 Year: 2021/n🎙️Language: English/n📊Rating: 6.8/10",
            reply_markup=reply_markup,
            parse_mode='html'
        
        )
    elif query.data == "ha1":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-NTRfNThfLTEwMDE2NTc2MjkyODVfL2JhdGNo")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/d39128d12108a114625fd.jpg",
            caption="""🎬 Title: Home Alone 1 
📅 Year: 1990 
🎙️Language: English Multi audio
📊Rating: 7.4/10""",
            reply_markup=reply_markup,
            parse_mode='html'
        
        )  

    elif query.data == "ha2":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-NTlfNjVfLTEwMDE2NTc2MjkyODVfL2JhdGNo")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/8beaabbd30f4dbf084f4e.jpg",
            caption="""🎬 Title: Home Alone 2 
📅 Year: 1992 
🎙️Language: English Multi audio 
📊Rating: 7.4/10""",
            reply_markup=reply_markup,
            parse_mode='html'
        
        )
    elif query.data == "ha3":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-NjZfNzFfLTEwMDE2NTc2MjkyODVfL2JhdGNo")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/e854ab3fdf212c4c154a0.jpg",
            caption="""🎬 Title: Home Alone 3 
📅 Year: 1997 
🎙️Language: English Multi audio 
📊Rating: 7.4/10""",
            reply_markup=reply_markup,
            parse_mode='html'
        
        )
    elif query.data == "ha4":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-NzJfNzZfLTEwMDE2NTc2MjkyODVfL2JhdGNo")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/97508660c08ed28f17823.jpg",
            caption="""🎬 Title: Home Alone 4 
📅 Year: 2002 
🎙️Language: English Multi audio 
📊Rating: 7.4/10""",
            reply_markup=reply_markup,
            parse_mode='html'
        
        )
    elif query.data == "ha5":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-NzdfODBfLTEwMDE2NTc2MjkyODVfL2JhdGNo")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/1d9db2e6c40d3e3e57992.jpg",
            caption="""🎬 Title: Home Alone 5 
📅 Year: 2012 
🎙️Language: English Multi audio 
📊Rating: 7.4/10""",
            reply_markup=reply_markup,
            parse_mode='html'
        
        )
    elif query.data == "ha6":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-ODFfODZfLTEwMDE2NTc2MjkyODVfL2JhdGNo")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/da6e500bd6589feb2b7df.jpg",
            caption="""🎬 Title: Home Alone 6 
📅 Year: 2021 
🎙️Language: English Multi audio 
📊Rating: 7.4/10""",
            reply_markup=reply_markup,
            parse_mode='html'
        
        )
    elif query.data == "vk1":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-ODdfOTdfLTEwMDE2NTc2MjkyODVfL2JhdGNo")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/751866aa416b3195d029c.jpg",
            caption="""🎬 Title: VIKINGS 01 
📅 Year: 2013
🎙️Language: English & Multi audio 
📊Rating: 9.4/80""",
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "vk2":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-OThfMTA5Xy0xMDAxNjU3NjI5Mjg1Xy9iYXRjaA")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/751866aa416b3195d029c.jpg",
            caption="""🎬 Title: VIKINGS 02 
📅 Year: 2014
🎙️Language: English & Multi audio 
📊Rating: 9.4/80""",
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "vk3":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-MTEwXzEyMV8tMTAwMTY1NzYyOTI4NV8vYmF0Y2g")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/751866aa416b3195d029c.jpg",
            caption="""🎬 Title: VIKINGS 03 
📅 Year: 2015
🎙️Language: English & Multi audio 
📊Rating: 9.4/80""",
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "vk4":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-MTIyXzE0M18tMTAwMTY1NzYyOTI4NV8vYmF0Y2g")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/751866aa416b3195d029c.jpg",
            caption="""🎬 Title: VIKINGS 04 
📅 Year: 2017
🎙️Language: English & Multi audio 
📊Rating: 9.4/80""",
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "vk5":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/c/1657629285/166")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/751866aa416b3195d029c.jpg",
            caption="""🎬 Title: VIKINGS 05 
📅 Year: 2019
🎙️Language: English & Multi audio 
📊Rating: 9.4/80""",
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "vk6":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-MTY3XzE3OF8tMTAwMTY1NzYyOTI4NV8vYmF0Y2g")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/751866aa416b3195d029c.jpg",
            caption="""🎬 Title: VIKINGS 06 
📅 Year: 2020
🎙️Language: English & Multi audio 
📊Rating: 9.4/80""",
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "vk7":
        buttons = [[
            InlineKeyboardButton('🔰 DOWNLOAD 🔰', url="https://t.me/lisamoviebot?start=DSTORE-MTc5XzIyMl8tMTAwMTY1NzYyOTI4NV8vYmF0Y2g")                     
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_photo(
            photo="https://telegra.ph/file/751866aa416b3195d029c.jpg",
            caption="""🎬 Title: VIKINGS 06 PART B
📅 Year: 2020
🎙️Language: English & Multi audio 
📊Rating: 9.4/80""",
            reply_markup=reply_markup,
            parse_mode='html'
        )
    
    elif query.data == "moviekittan":   
        buttons = [[
            InlineKeyboardButton("ʟᴀᴛᴇꜱᴛ ᴍᴏᴠɪᴇꜱ ᴄʜᴀɴɴᴇʟ", url='t.me/cinemakodathi')
        ],[
            InlineKeyboardButton("ᴄɪɴᴇᴍᴀ ᴋᴏᴅᴀᴛʜɪ", url='t.me/cinemakodathi')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MOVIE_KITTAN.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode='html'
        )

    elif query.data == "mfk2":
        buttons = [[
            InlineKeyboardButton('ꜱᴇᴀʀᴄʜ ᴍᴏᴠɪᴇꜱ ᴄʟɪᴄᴋ ʜᴇʀᴇ', switch_inline_query_current_chat='')
        ],[
            InlineKeyboardButton('ʜᴏᴍᴇ', callback_data="start"),
            InlineKeyboardButton('ᴄʟᴏꜱᴇ', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SERCH_MOVIE.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode='html'
        )
            
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('Manual Filter', callback_data='manuelfilter'),
            InlineKeyboardButton('Auto Filter', callback_data='autofilter')
        ], [
            InlineKeyboardButton('Connection', callback_data='coct'),
            InlineKeyboardButton('Extra Mods', callback_data='extra')
        ], [
            InlineKeyboardButton('🏠 Home', callback_data='start'),
            InlineKeyboardButton('🔮 Status', callback_data='stats')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "about":
        buttons = [[
            InlineKeyboardButton('🤖 Updates', url='https://t.me/TeamEvamaria'),
            InlineKeyboardButton('♥️ Source', callback_data='source')
        ], [
            InlineKeyboardButton('🏠 Home', callback_data='start'),
            InlineKeyboardButton('🔐 Close', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "tip3": 
          await query.answer(f" • ബ്രോ ഇതിലല്ല 😃 \n\n • താഴെ വരുന്ന മൂവി ലിസ്റ്റിലാണ് ഞെക്കേണ്ടത്😁",show_alert=True)
    elif query.data == "getmovie": 
          await query.answer(f" ➪ നിങ്ങൾ ബോട്ടിന്റെ മെയിൻ ചാനലിൽ ജോയിൻ ചെയ്തിട്ടില്ല അതാണ് നിങ്ങൾക് സിനിമ കിട്ടാത്തത്  😃 \n\n ➪ മെയിൻ ചാനൽ link കിട്ടാൻ നിങ്ങൾ /clink എന്ന് മെസ്സേജ്  അയച്ചാൽ മതി 😁",show_alert=True)
    elif query.data == "searchfile": 
          await query.answer(f" ➪ inline ആയി മൂവി സെർച്ച്‌ ചെയ്യാൻ നിങ്ങൾ ബോട്ടിൽ /start എന്ന് അടിക്കുക \n\n ➪ ബോട്ട് റിപ്ലേ തരുന്ന മെസ്സേജിൽ ꜱᴇᴀʀᴄʜ ᴍᴏᴠɪᴇꜱ എന്ന ബട്ടണിൽ ക്ലിക്ക് ചയ്യുക",show_alert=True)
    elif query.data == "commamds": 
          await query.answer(f" ➪ നിങ്ങൾക്ക് ഇ ബോട്ടിൽ ലബ്യമായിട്ടുള്ള കമാണ്ടുകൾ കാണണം എങ്കിൽ /command എന്ന് മെസ്സേജ് ഇടുക",show_alert=True)
    elif query.data == "enqury": 
          await query.answer(f" ➪ നിങ്ങൾക് എന്തെങ്കിലും പറയാനുണ്ടേൽ admin ആയി ബന്ധപെടേണ്ടത് ആണ്",show_alert=True)
    elif query.data == "source":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "manuelfilter":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('⏹️ Buttons', callback_data='button')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MANUELFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "button":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='manuelfilter')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BUTTON_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CONNECTION_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "extra":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('👮‍♂️ Admin', callback_data='admin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.EXTRAMOD_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "admin":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='extra')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ADMIN_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('♻️', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('♻️', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("Your Active Connection Has Been Changed. Go To /settings.")
            return await query.answer('Piracy Is Crime')

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Filter Button',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Single' if settings["button"] else 'Double',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Bot PM', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["botpm"] else '❌ No',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('File Secure',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["file_secure"] else '❌ No',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('IMDB', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["imdb"] else '❌ No',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Spell Check',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["spell_check"] else '❌ No',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Welcome', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["welcome"] else '❌ No',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)
    await query.answer('Piracy Is Crime')


async def auto_filter(client, msg, spoll=False):
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if 2 < len(message.text) < 100:
            search = message.text
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:
                if settings["spell_check"]:
                    return await advantage_spell_chok(msg)
                else:
                    return
        else:
            return
    else:
        settings = await get_settings(msg.message.chat.id)
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"📂{get_size(file.file_size)} 📂{file.file_name}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}",
                    callback_data=f'{pre}#{file.file_id}',
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'{pre}_#{file.file_id}',
                ),
            ]
            for file in files
        ]

    if offset != "":
        key = f"{message.chat.id}-{message.message_id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton(text=f"🗓 1/{round(int(total_results) / 10)}", callback_data="pages"),
             InlineKeyboardButton('🗑', callback_data='close_data'),
             InlineKeyboardButton(text="NEXT ⏩", callback_data=f"next_{req}_{key}_{offset}")]   
        )
        btn.insert(0,
            [InlineKeyboardButton(text="⭕️ 𝗝𝗢𝗜𝗡 𝗠𝗬 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 ⭕️",url="https://t.me/moviesupdateck")]
        )
        btn.insert(0,
            [InlineKeyboardButton(text=f"🔮 {msg.text} ",callback_data="imd_alert"),
             InlineKeyboardButton(text=f"🗂 {total_results} ",callback_data="tip2")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="🗓 1/1", callback_data="pages")]
        )
        btn.insert(0,
            [InlineKeyboardButton(text="⭕️ 𝗝𝗢𝗜𝗡 𝗠𝗬 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 ⭕️",url="https://t.me/moviesupdateck")]
        )
        btn.insert(0,
            [InlineKeyboardButton(text=f"🔮 {msg.text} ",callback_data="imd_alert"),
             InlineKeyboardButton(text=f"🗂 {total_results} ",callback_data="tip2")]
        )
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
            query=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
    else:
        cap = f"""Hey 👋 {message.from_user.mention}😍

 📁 ғᴏᴜɴᴅ ✨ ғɪʟᴇs ғᴏʀ ʏᴏᴜʀ ǫᴜᴇʀʏ : #{search} 👇"""
    if imdb and imdb.get('poster'):
        try:
            await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024],
                                      reply_markup=InlineKeyboardMarkup(btn))
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
        except Exception as e:
            logger.exception(e)
            await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
    if spoll:
        await msg.message.delete()



async def advantage_spell_chok(msg):
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words
    query = query.strip() + " movie"
    g_s = await search_gagala(query)
    g_s += await search_gagala(msg.text)
    gs_parsed = []
    if not g_s:
        k = await msg.reply("I couldn't find any movie in that name.")
        await asyncio.sleep(8)
        await k.delete()
        return
    regex = re.compile(r".*(imdb|wikipedia).*", re.IGNORECASE)  # look for imdb / wiki results
    gs = list(filter(regex.match, g_s))
    gs_parsed = [re.sub(
        r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)',
        '', i, flags=re.IGNORECASE) for i in gs]
    if not gs_parsed:
        reg = re.compile(r"watch(\s[a-zA-Z0-9_\s\-\(\)]*)*\|.*",
                         re.IGNORECASE)  # match something like Watch Niram | Amazon Prime
        for mv in g_s:
            match = reg.match(mv)
            if match:
                gs_parsed.append(match.group(1))
    user = msg.from_user.id if msg.from_user else 0
    movielist = []
    gs_parsed = list(dict.fromkeys(gs_parsed))  # removing duplicates https://stackoverflow.com/a/7961425
    if len(gs_parsed) > 3:
        gs_parsed = gs_parsed[:3]
    if gs_parsed:
        for mov in gs_parsed:
            imdb_s = await get_poster(mov.strip(), bulk=True)  # searching each keyword in imdb
            if imdb_s:
                movielist += [movie.get('title') for movie in imdb_s]
    movielist += [(re.sub(r'(\-|\(|\)|_)', '', i, flags=re.IGNORECASE)).strip() for i in gs_parsed]
    movielist = list(dict.fromkeys(movielist))  # removing duplicates
    if not movielist:
        k = await msg.reply("I couldn't find anything related to that. Check your spelling")
        await asyncio.sleep(8)
        await k.delete()
        return
    SPELL_CHECK[msg.message_id] = movielist
    btn = [[
        InlineKeyboardButton(
            text=movie.strip(),
            callback_data=f"spolling#{user}#{k}",
        )
    ] for k, movie in enumerate(movielist)]
    btn.append([InlineKeyboardButton(text="Close", callback_data=f'spolling#{user}#close_spellcheck')])
    await msg.reply(f"""➪Hey👋 {msg.from_user.mention} 

➪I couldn't find anything related to that

➪Did you mean any one of these?""",
                    reply_markup=InlineKeyboardMarkup(btn))

async def manual_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await client.send_message(group_id, reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                    elif btn == "[]":
                        await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                    else:
                        button = eval(btn)
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False
