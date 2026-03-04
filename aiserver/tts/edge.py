import edge_tts

class Edge_TTS:

    def __init__(self, config):
        self.voice = config.get("voice")

    # 文字转语音
    async def text_to_speech(self, text, audio_path):
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(audio_path)
        return audio_path