from pyrogram import Client, filters
import youtube_dl
from youtube_search import YoutubeSearch
import requests

import os
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))

@Client.on_message(filters.command(['song']))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('`Searching... Please Wait...`')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            performer = f"[ミ★ 𝘏𝘰𝘯𝘦𝘺 𝘉𝘦𝘦 𝘔𝘶𝘴𝘪𝘤 ★彡]" 
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('**Found Literary Nothing. Please Try Another Song or Use Correct Spelling Nanba!**')
            return
    except Exception as e:
        m.edit(
            "**Enter Song Name with Command!**"
        )
        print(str(e))
        return
    m.edit("`Uploading... Please Wait...`")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🏷 <b>Title:</b> <a href="{link}">{title}</a>\n⏳ <b>Duration:</b> <code>{duration}</code>\n👀 <b>Views:</b> <code>{views}</code>\n🎧 <b>Uploaded By:</b> <a href="https://t.me/honeybeemovies">ミ★ 𝘏𝘰𝘯𝘦𝘺 𝘉𝘦𝘦 𝘔𝘶𝘴𝘪𝘤 ★彡</a>'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
        message.delete()
    except Exception as e:
        m.edit('**An Error Occured !!**')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
