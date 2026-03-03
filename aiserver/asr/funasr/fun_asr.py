import os
import librosa
from funasr import AutoModel


class Funasr:
    def __init__(self):
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
        return res

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    funasr = Funasr()
    res = funasr.audio_file_to_text("test.wav")
    print(res)