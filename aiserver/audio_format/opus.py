import os
import pickle
import wave
from typing import List

import numpy as np
import opuslib_next
from pydub import AudioSegment

# 该类用于对音频进行opus编码
# 初始化了音频提取参数与opus编码参数
class Opus_Encode:
    _instance = None
    # 单例模式
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        self.sample_rate = 16000
        self.channel = 1
        self.sample_width = 2
        self.opus_sample_rate = 16000  # 采样率/ Hz
        self.opus_channel = 1
        self.opus_frame_time = 60  # 帧时长/ ms
        self.opus_sample_width = 2  # 采样宽度/ 字节，16bit
        # 计算opus每帧采样数量
        self.opus_frame_size = int(self.opus_sample_rate / 1000 * self.opus_frame_time)
        # 计算opus每帧占用字节
        self.opus_frame_bytes_size = self.opus_frame_size * self.opus_channel * self.opus_sample_width

    # _________________________________________wav/mp3 -> opus  encode_________________________________________
    def audio_to_opus(self, audio_file_path):
        # ##########################获取音频参数####################
        # os.path.splitext方法获取音频格式
        file_type = os.path.splitext(audio_file_path)[1]
        if file_type:
            file_type = file_type.lstrip(".")
        # AudioSegment.from_file方法,根据音频格式，解析音频参数
        audio = AudioSegment.from_file(audio_file_path, format=file_type)
        # 调整音频参数
        audio = audio.set_channels(self.channel).set_frame_rate(self.sample_rate).set_sample_width(self.sample_width)
        # 计算音频时长
        duration = len(audio)
        # 计算音频大小
        raw_datas = audio.raw_data

        # ####################opus编码器设置####################
        encoder = opuslib_next.Encoder(self.opus_sample_rate, self.opus_channel, opuslib_next.APPLICATION_AUDIO)
        # 每帧采样数量
        frame_num = self.opus_frame_size
        # 每帧占用字节
        frame_bytes_size = self.opus_frame_bytes_size
        # 创建一个空列表，存储Opus数据帧
        opus_datas = []

        # ######################按帧编码#######################
        # 按帧字节分割raw_data为数据块
        for i in range(0, len(raw_datas), frame_bytes_size):
            chunk = raw_datas[i:i + frame_bytes_size]
            # 末块添加二进制零
            chunk_len = len(chunk)
            if chunk_len < frame_bytes_size:
                chunk += b'\x00' * (frame_bytes_size - chunk_len)

            # 数据块由二进制转换为NumPy数组
            np_frame = np.frombuffer(chunk, dtype=np.int16)
            # NumPy数组重新转换为二进制
            np_bytes = np_frame.tobytes()

            # 使用编码器对二进制数据块进行opus编码。
            # frame_num参数指定每帧的采样数
            opus_data = encoder.encode(np_bytes, frame_num)
            # Opus数据帧添加至空列表
            opus_datas.append(opus_data)

    # 最终返回完整的opus编码和时长
        return opus_datas

    # ___________________________________________ Opus_dates <-->.opus ________________________________________________
    # 该方法将opus编码帧列表保存为二进制文件（利用pickle.dump方法）
    def save_opus_raw(self, opus_select, output_path):
        with open(output_path, "wb") as f:
            pickle.dump(opus_select, f)
    # 该方法读取二进制文件，最终返回opus编码帧列表
    def load_opus_raw(self, input_path):
        with open(input_path, "rb") as f:
            opus_datas = pickle.load(f)
        return opus_datas

    # ________________________________________ Opus->wav ____________________________________________
    # 传入opus编码帧列表，返回wav文件路径
    def opus_to_wav_file(self, output_file, opus_data : List[bytes]) -> str:

        # 创建一个解码器
        decoder = opuslib_next.Decoder(self.opus_sample_rate, self.opus_channel)
        # 创建一个空列表，存储PCM数据帧
        pcm_data = []

        # 遍历Opus数据帧
        for frame in opus_data:
            try:
                # 解码Opus数据帧
                pcm_frame = decoder.decode(frame, self.opus_frame_size)
                # 将PCM数据帧添加至空列表
                pcm_data.append(pcm_frame)
            # 捕获解码失败的异常
            except opuslib_next.OpusError as e:
                print(f"解码失败: {e}")

        # 创建一个WAV文件（输出output_file为test.wav）
        with wave.open(output_file, "wb") as wav_file:
            # 设置WAV文件的参数
            wav_file.setnchannels(self.opus_channel)
            wav_file.setsampwidth(self.opus_sample_width)
            wav_file.setframerate(self.opus_sample_rate)
            # 将PCM数据帧写入WAV文件
            wav_file.writeframes(b''.join(pcm_data))

        return output_file


if __name__ == "__main__":
    # test.mp3编码测试
    opus = Opus_Encode()
    opus_output = opus.audio_to_opus("../../test.mp3")

    print(f"Opus数据帧数：{len(opus_output)}")
    print(f"二进制编码：")
    print(opus_output)

    # opus_output读写测试
    # 将opus帧列表写为.opus文件
    opus.save_opus_raw(opus_output, "test.opus")
    # 读.opus文件，返回opus帧列表
    load = opus.load_opus_raw("test.opus")
    print(load)

    # load解码测试
    # 将返回的opus帧列表保存为.wav文件
    opus.opus_to_wav_file("test.wav", load)