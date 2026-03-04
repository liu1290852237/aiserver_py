import os
import librosa
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

from aiserver.audio_format.opus import Opus_Encode
from aiserver.utils.util import Util


class Funasr:
    def __init__(self, config):
        # 获取输出目录
        self.dir = config.get("output_dir")
        # 获取当前目录
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        # 拼接出模型的路径
        self.model_dir = os.path.join(self.current_dir, "model")
        # 创建模型
        self.model = AutoModel(
            model=self.model_dir,
            vad_kwargs={"max_single_segment_time": 30000},
            # device="cuda:0"
            disable_update=True,
            hub="hf",
            trust_remote_code=True,
        )

    def audio_file_to_text(self, file_path):
        res = self.model.generate(
            input=file_path,
            language="auto",
        )
        ress = res[0]["text"]
        return rich_transcription_postprocess(ress)

    # 混合方法。引入Opus_Encode把帧列表解码为.wav，配合Funasr把.wav转换为text。
    # a shit
    def mix_opus_to_text(self, opus_dates, wav_file):
        opus = Opus_Encode()
        # 将opus帧列表保存为.wav文件
        opus.opus_to_wav_file(wav_file, opus_dates)
        # 将.wav文件转为文本
        self.audio_file_to_text(wav_file)


if __name__ == "__main__":
    # 切换至当前目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 调用 Util.get_config() 来加载配置
    config = Util.get_config()

    funasr = Funasr(config.get("ASR").get("Fun_ASR"))
    res = funasr.audio_file_to_text("test.wav")
    print(res)