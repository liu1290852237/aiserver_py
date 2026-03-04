import asyncio
import os

from aiserver.asr.funasr.fun_asr import Funasr
from aiserver.audio_format.opus import Opus_Encode
from aiserver.llm.GLM import GLM
from aiserver.tts.edge import Edge_TTS
from aiserver.utils.util import Util

if __name__ == "__main__":
    # 解析配置文件
    config = Util.get_config()
    # 类实体化
    llm = GLM(config.get("LLM").get("ChatGLM"))
    edge_tts = Edge_TTS(config.get("TTS").get("EdgeTTS"))
    opus_encode = Opus_Encode()
    funasr = Funasr(config.get("ASR").get("Fun_ASR"))

    """该测试，先向模型输入提问text，代替esp32的asr过程，测试tts；将得到的回答mp3作为esp32的提问，测试asr"""
    """接收回答"""
    # 把提问txt提交至模型，获取回答txt
    resource = llm.generate_response("你是谁")  # ask->reply  llm
    print(resource)

    # 后端把回答txt合成回答mp3
    output_file = asyncio.run(edge_tts.text_to_speech(resource, "test.mp3"))  # txt->mp3  tts

    # 后端编码回答mp3，发送
    opus_dates_reply = opus_encode.audio_to_opus("test.mp3")  # mp3->opus  encode
    # (接下来由esp32接收并实现解码) opus=>esp=>speaker

    """发出提问"""
    # (该步骤应由esp32编码并发送) micro=>esp=>opus
    opus_dates_ask = opus_encode.audio_to_opus("test.mp3")

    # 后端解码帧列表，得到提问wav
    opus_encode.opus_to_wav_file("retest.wav", opus_dates_ask)  # opus->wav  decode

    # 后端从提问wav识别提问txt，提交至模型
    resource = funasr.audio_file_to_text("retest.wav")  # wav->txt  asr
    print(resource)