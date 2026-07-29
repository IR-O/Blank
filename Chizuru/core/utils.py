from youtube_search import YoutubeSearch
import yt_dlp

async def search_song(query):
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        if results:
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
            
            return {
                'link': f"https://youtube.com{results[0]['url_suffix']}",
                'title': results[0]['title'],
                'thumbnail': results[0]['thumbnails'][0],
                'duration': duration,
                'duration_sec': dur_sec,
                'views': results[0]['views']
            }
        return None
    except Exception as e:
        print(f"Search error: {e}")
        return None

async def get_audio_stream(link):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web', 'ios'],
                }
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            return info.get('url')
    except Exception as e:
        print(f"Stream error: {e}")
        return None

async def get_video_stream(link):
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            return info.get('url')
    except Exception as e:
        print(f"Video stream error: {e}")
        return None

class Queue:
    def __init__(self):
        self.queues = {}
    
    async def put(self, chat_id, file_path, song_info):
        if chat_id not in self.queues:
            self.queues[chat_id] = []
        self.queues[chat_id].append({'file': file_path, 'info': song_info})
        return len(self.queues[chat_id])
    
    async def get(self, chat_id):
        if chat_id in self.queues and self.queues[chat_id]:
            return self.queues[chat_id].pop(0)
        return None
    
    async def is_empty(self, chat_id):
        if chat_id in self.queues:
            return len(self.queues[chat_id]) == 0
        return True
    
    async def clear(self, chat_id):
        if chat_id in self.queues:
            self.queues[chat_id].clear()

queue = Queue()
