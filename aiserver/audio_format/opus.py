import os

import numpy as np
import opuslib_next
from pydub import AudioSegment

class Opus_Encode:
    def __init__(self):
        self.sample_rate = 16000
        self.channel = 1
        self.sample_width = 2
        self.opus_sample_rate = 16000  # 采样率/ Hz
        self.opus_channels = 1
        self.opus_frame_time = 60  # 帧时长/ ms
        self.opus_sample_width = 2  # 采样宽度/ 字节，16bit
    def audio_to_opus(self, audio_file_path):

        # 获取音频格式
        file_type = os.path.splitext(audio_file_path)[1]
        if file_type:
            file_type = file_type.lstrip(".")
        # 加载音频文件
        audio = AudioSegment.from_file(audio_file_path, format=file_type)

        # 设置音频参数
        audio = audio.set_channels(self.channel).set_frame_rate(self.sample_rate).set_sample_width(self.sample_width)

        # 计算音频时长
        duration = len(audio)

        # 获取音频PCM数据
        raw_data = audio.raw_data
        print(f"音频PCM数据大小：{len(raw_data)}字节")

        # encoder编码器设置
        encoder = opuslib_next.Encoder(self.opus_sample_rate, self.opus_channels, opuslib_next.APPLICATION_AUDIO)

        # 计算每帧的采样数
        frame_num = int(self.opus_sample_rate / 1000 * self.opus_frame_time)

        # 计算每帧的采样字节数
        frame_bytes_size = frame_num * self.opus_channels * self.sample_width

        opus_datas = []
        # 按帧字节分割raw_data数据
        for i in range(0, len(raw_data), frame_bytes_size):
            chunk = raw_data[i:i + frame_bytes_size]

            # 末帧添加二进制零
            chunk_len = len(chunk)
            if chunk_len < frame_bytes_size:
                chunk += b'\x00' * (frame_bytes_size - chunk_len)

            # 将二进制音频数据块转换为NumPy数组
            np_frame = np.frombuffer(chunk, dtype=np.int16)
            # 将上一步得到的NumPy数组重新转换为字节数据
            np_bytes = np_frame.tobytes()

            # 使用Opus编码器对字节数据np_bytes进行编码。 frame_num参数指定每帧的采样数
            opus_data = encoder.encode(np_bytes, frame_num)
            # 将编码后的Opus数据帧添加至列表opus_datas中
            opus_datas.append(opus_data)

        return opus_datas, duration

if __name__ == "__main__":
    opus = Opus_Encode()
    opus_data, duration = opus.audio_to_opus("../../test.mp3")

    print(f"音频总时长：{duration}毫秒")
    print(f"编码后的Opus数据帧数：{len(opus_data)}")
    print(opus_data)