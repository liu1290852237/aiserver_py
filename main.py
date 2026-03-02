import asyncio
import os

from aiserver.llm.GLM import GLM
from aiserver.tts.edge import Edge_TTS

if __name__ == "__main__":
    # 实例化glm
    llm = GLM()
    # 调用方法，传入问题，生成回复
    resource = llm.generate_response("你在干嘛?")

    # 实例化tts
    tts = Edge_TTS()
    # 调用方法，传入回复，合成语音
    output_file = asyncio.run(tts.text_to_speech(resource, "test.mp3"))

    # windows播放
    os.system(f"start {output_file}")
    print(resource)