from youtube_search import YoutubeSearch
import yt_dlp

class YouTube:
    @staticmethod
    async def search(query, video=False):
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            if not results:
                return None
            
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]['title']
            duration = results[0]['duration']
            
            dur_sec = 0
            try:
                parts = duration.split(':')
                if len(parts) == 2:
                    dur_sec = int(parts[0]) * 60 + int(parts[1])
                elif len(parts) == 3:
                    dur_sec = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            except:
                dur_sec = 0
            
            stream_url = await YouTube.get_stream(link, video)
            if not stream_url:
                return None
            
            return {
                'url': link,
                'title': title,
                'duration': duration,
                'duration_sec': dur_sec,
                'file_path': stream_url
            }
        except Exception as e:
            print(f"Search error: {e}")
            return None

    @staticmethod
    async def get_stream(link, video=False):
        try:
            format_type = 'bestvideo+bestaudio/best' if video else 'bestaudio/best'
            ydl_opts = {
                'format': format_type,
                'quiet': True,
                'no_warnings': True,
                'extractor_args': {
                    'youtube': {'player_client': ['android', 'web', 'ios']}
                }
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                return info.get('url')
        except Exception as e:
            print(f"Stream error: {e}")
            return None

yt = YouTube()

# Queue management
queues = {}

class Queue:
    @staticmethod
    async def add(chat_id, song_data):
        if chat_id not in queues:
            queues[chat_id] = []
        queues[chat_id].append(song_data)
        return len(queues[chat_id])

    @staticmethod
    async def get(chat_id):
        if chat_id in queues and queues[chat_id]:
            return queues[chat_id].pop(0)
        return None

    @staticmethod
    async def get_all(chat_id):
        if chat_id in queues:
            return queues[chat_id]
        return []

    @staticmethod
    async def clear(chat_id):
        if chat_id in queues:
            queues[chat_id] = []

    @staticmethod
    async def is_empty(chat_id):
        if chat_id in queues:
            return len(queues[chat_id]) == 0
        return True

queue = Queue()
