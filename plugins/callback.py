from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, emoji
from datetime import datetime, timedelta
from utils.vc import mp
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "replay":
        group_call = mp.group_call
        if not mp.playlist:
            return
        group_call.restart_playout()
        await mp.update_start_time()
        start_time = mp.start_time
        playlist = mp.playlist
        if not start_time:
            await query.edit_message_text(f"{emoji.PLAY_BUTTON} **Onnum Playcheyunilla ! He he**")
            return
        utcnow = datetime.utcnow().replace(microsecond=0)
        if mp.msg.get('current') is not None:
            playlist=mp.playlist
            if not playlist:
                pl = f"{emoji.NO_ENTRY} **Playlist Empty Aanallo!**"
            else:
                if len(playlist) == 1:
                    pl = f"{emoji.REPEAT_SINGLE_BUTTON} **Playlist**:\n"
                else:
                    pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n"
                pl += "\n".join([
                    f"**{i}**. **{x.audio.title}**"
                    for i, x in enumerate(playlist)
                    ])
            await mp.msg['current'].delete()
            mp.msg['current'] = await playlist[0].reply_text(
                f"{pl}\n\n{emoji.PLAY_BUTTON}  {utcnow - start_time} / "
                f"{timedelta(seconds=playlist[0].audio.duration)}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏸", callback_data="pause"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data == "pause":
        mp.group_call.pause_playout()
        await mp.update_start_time(reset=True)
        playlist = mp.playlist
        if not playlist:
            pl = f"{emoji.NO_ENTRY} **Playlist Empty Aanallo!**"
        else:
            if len(playlist) == 1:
                pl = f"{emoji.REPEAT_SINGLE_BUTTON} **Playlist**:\n"
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n"
            pl += "\n".join([
                f"**{i}**. **{x.audio.title}**"
                for i, x in enumerate(playlist)
                ])
        reply = await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} **Paused aakitund ketta!**\n\n{pl}",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("▶️", callback_data="resume"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    
    elif query.data == "resume":
        mp.group_call.resume_playout()
        playlist=mp.playlist
        if not playlist:
            pl = f"{emoji.NO_ENTRY} **Empty Playlist!**"
        else:
            if len(playlist) == 1:
                pl = f"{emoji.REPEAT_SINGLE_BUTTON} **Playlist**:\n"
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n"
            pl += "\n".join([
                f"**{i}**. **{x.audio.title}**"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} **baaki Iduaney!**\n\n{pl}",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏸", callback_data="pause"),
                            InlineKeyboardButton("⏩", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data=="skip":
        playlist = mp.playlist
        await mp.skip_current_playing()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} **Empty Playlist!**"
        else:
            if len(playlist) == 1:
                pl = f"{emoji.REPEAT_SINGLE_BUTTON} **Playlist**:\n"
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n"
            pl += "\n".join([
                f"**{i}**. **{x.audio.title}**"
                for i, x in enumerate(playlist)
                ])

        try:
            await query.edit_message_text(f"⏭ **Skipped Cheyth! Ki ki**\n\n{pl}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔄", callback_data="replay"),
                        InlineKeyboardButton("⏸", callback_data="pause"),
                        InlineKeyboardButton("⏩", callback_data="skip")
                            
                    ],
                ]
            )
        )
        except:
            pass
    elif query.data=="help":
        await query.edit_message_text("🙋‍♂️ **Hi Monu **, \n Gummaru Tappuru. Gummaru Tappuru. Gummaru Tappuru. Gummaru Tappuru Gummaru Gummaru Gummaru Gummaru raa! 😌\n\nCheck /help To Know More ...")

