from gtts import gTTS 
import os
import hashlib
def text_to_speech(text,lang_name):
    try:
        cache_dir=os.path.join('static','4_cache')
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        lang_map={'Hindi':'hi','Malayalam':'ml','Tamil':'ta','Telegu':'te','English':'en'}
        lang_code=lang_map.get(lang_name,'en')
        unique_str=f"{text}_{lang_code}"
        file_hash=hashlib.md5(unique_str.encode()).hexdigest()
        filename=f"tts_{file_hash}.mp3"
        filepath=os.path.join(cache_dir,filename)
        if os.path.exists(filepath):
            return f"audio_cache/{filename}"
        tts=gTTS(text=text,lang=lang_code,slow=False)
        tts.save(filepath)
        return f"audio_cache/{filename}"
    except Exception as e:
        print(f"TTS Error:{e}")
        return None
        