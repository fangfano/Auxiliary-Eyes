import os
import appbuilder
from API_KEY import *
import pyaudio
import wave
from utils.llm import llm_qwen

class TextToSpeech:
    def __init__(self):
        self.tts_ab = appbuilder.TTS()

    def synthesize_to_wav(self, text='你好', output_path='temp/tts.wav'):
        '''
        语音合成TTS，生成wav音频文件
        '''
        message = appbuilder.Message(content={"text": text})
        result = self.tts_ab.run(message, model="paddlespeech-tts", audio_type="wav")
        with open(output_path, "wb") as f:
            f.write(result.content["audio_binary"])
        # print("TTS语音合成，导出wav音频文件至：{}".format(output_path))

class AudioPlayer:
    @staticmethod
    def play_wav(file_path='asset/welcome.wav'):
        '''
        播放wav音频文件
        '''
        command = 'aplay -t wav {} -q'.format(file_path)
        os.system(command)


def say_hello():
    # 播放welcome音频
    text_to_speech = TextToSpeech() # 创建 TextToSpeech 和 AudioPlayer 实例
    text_to_speech.synthesize_to_wav("欢迎使用智目", output_path="temp/welcome.wav")
    AudioPlayer.play_wav('temp/welcome.wav')