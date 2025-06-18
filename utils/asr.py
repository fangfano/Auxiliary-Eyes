
import pyaudio
from pydub import AudioSegment


import wave
import numpy as np
import os
import sys
import time
from collections import deque


# Initialize audio once
audio = pyaudio.PyAudio()
# Find card 1's index (run this once)
card1_index = -1
for i in range(audio.get_device_count()):
    dev_info = audio.get_device_info_by_index(i)
    if dev_info['maxInputChannels'] > 0 and "USB ENC Audio Device" in dev_info['name']:
        card1_index = i
        print("USB ENC Audio Device is: ", card1_index)
        break
if card1_index == -1:
    print("USB ENC Audio Device not found!")
# 获取设备信息
print("Audio Device ID: ",card1_index)
dev_info = audio.get_device_info_by_index(card1_index)
supported_rates = int(dev_info.get("defaultSampleRate", 16000))




def record(DURATION=5):
    '''
    调用麦克风录音，需用arecord -l命令获取麦克风ID
    DURATION，录音时长
    '''
    # print('开始 {} 秒录音'.format(DURATION))
    print('开始录音')
    os.system('arecord -D "plughw:{}" -f dat -c 1 -r 16000 -d {} temp/speech_record.wav'.format(card1_index, DURATION))
    print('录音结束')



def record_until_silence(output_filename="temp/speech_record.wav", 
                         rate=supported_rates, chunk=1024, format=pyaudio.paInt16, channels=1,
                         noise_sample_time=0.5, max_silence_wait=5.0, silence_duration=2.0):
    """
    根据麦克风输入的音频音量判断用户是否结束说话
    
    参数:
    - output_filename: 输出音频文件名
    - rate: 采样率
    - chunk: 每次读取的帧数
    - format: 音频格式
    - channels: 通道数
    - noise_sample_time: 采样环境噪音的时间(秒)
    - max_silence_wait: 最大等待时间(秒)，如果超过此时间没有检测到声音则退出
    - silence_duration: 静音持续时间(秒)，超过该时间认为用户已结束说话
    
    返回:
    - bool: 如果成功检测到用户结束说话并保存音频，返回True
    """
    p = pyaudio.PyAudio()
    
    # 打开音频流
    stream = p.open(format=format,
                    channels=channels,
                    rate=supported_rates,
                    input=True,
                    frames_per_buffer=chunk,
                    input_device_index= card1_index  # 使用默认设备
                    )
    
    print("正在采样环境噪音...")
    
    # 存储音频帧 - 将存储所有的音频数据
    all_frames = []
    
    # 采样环境噪音
    noise_samples = []
    frames_to_sample = int(noise_sample_time * rate / chunk)
    
    for _ in range(frames_to_sample):
        data = stream.read(chunk)
        all_frames.append(data)  # 保存所有数据
        audio_data = np.frombuffer(data, dtype=np.int16)
        volume_norm = np.abs(audio_data).mean() / 32767.0
        noise_samples.append(volume_norm)
    
    # 计算噪音阈值 - 使用平均值加上一个标准差
    noise_threshold = np.mean(noise_samples) + np.std(noise_samples)
    # 设置一个最小阈值，避免极安静环境下阈值过低
    noise_threshold = max(noise_threshold, 0.01)
    
    print(f"环境噪音阈值设定为: {noise_threshold:.6f}")
    print("开始录音，请说话...")
    
    # 记录状态变量
    silent_since = None          # 记录开始静音的时间
    recording_started = False    # 是否已经开始录音
    start_time = time.time()     # 开始监听的时间
    speech_start_index = None    # 说话开始的帧索引
    speech_end_index = None      # 说话结束的帧索引
    start_record_filter_count = 0

    try:
        while True:
            # 读取音频数据
            data = stream.read(chunk)
            current_frame_index = len(all_frames)
            all_frames.append(data)
            
            # 计算音量
            audio_data = np.frombuffer(data, dtype=np.int16)
            volume_norm = np.abs(audio_data).mean() / 32767.0
            
            # 打印音量，便于调试
            print(f"音量: {volume_norm:.6f}, 阈值: {noise_threshold:.6f}")
            
            # 检测是否有声音
            if volume_norm > noise_threshold:
                if not recording_started:
                    start_record_filter_count+=1
                    if(start_record_filter_count >= 3):
                        recording_started = True
                        speech_start_index = current_frame_index
                        print(f"检测到声音，开始录音 (帧索引: {speech_start_index})")                    

                silent_since = None
            elif recording_started:
                # 如果当前是静音
                if silent_since is None:
                    silent_since = time.time()
                elif time.time() - silent_since > silence_duration:
                    # 如果静音持续了足够长的时间
                    speech_end_index = current_frame_index
                    print(f"检测到{silence_duration}秒的静音，录音结束 (帧索引: {speech_end_index})")
                    break
            elif not recording_started and (time.time() - start_time > max_silence_wait):
                # 如果超过最大等待时间仍未检测到声音，则退出
                print(f"等待{max_silence_wait}秒未检测到声音，退出录音")
                break
            else:
                    start_record_filter_count = 0
    
    except KeyboardInterrupt:
        print("录音被用户中断")
    
    finally:
        # 停止并关闭流
        stream.stop_stream()
        stream.close()
        p.terminate()
    
    # 如果成功录到音频，保存文件
    if recording_started and speech_start_index is not None and speech_end_index is not None:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(output_filename)), exist_ok=True)
        
        # 只保存从说话开始到说话结束的音频帧
        speech_frames = all_frames[speech_start_index:speech_end_index - 10]
        
        # 保存音频文件
        wf = wave.open(output_filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(speech_frames))
        wf.close()
        
        print(f"音频已保存到 {output_filename}")

        audio = AudioSegment.from_file(output_filename)
        audio = audio.set_frame_rate(16000)  # 设置目标采样率
        audio.export(output_filename, format="wav", parameters=["-ar", "16000"])

        print(f"录音长度: {len(speech_frames)/rate*chunk:.2f}秒")
        return {"status": True, "msg": f"音频已保存到 {output_filename}"}
    
    # print("未录制到有效音频")
    return {"status": False, "msg": "未录制到有效音频"}




from API_KEY import *
import appbuilder
import soundfile as sf
import librosa


# 配置密钥
os.environ["APPBUILDER_TOKEN"] = APPBUILDER_TOKEN
asr = appbuilder.ASR() # 语音识别组件
def speech_recognition(audio_path='./temp/speech_record.wav'):
    '''
    AppBuilder-SDK语音识别组件
    '''
    print('开始语音识别')

    audio_path_16k = './temp/speech_record_16k.wav'
    # 直接读取原始数据及采样率
    data, sr = sf.read(audio_path)  # 自动识别48kHz 
    # 重采样
    data_16k = librosa.resample(data.T, orig_sr=sr, target_sr=16000)  # 转置处理多声道 
    # 保存（自动处理多声道）
    sf.write(audio_path_16k, data_16k.T, 16000)  # 


    # 载入wav音频文件
    with wave.open(audio_path_16k, 'rb') as wav_file:
        
        # 获取音频文件的基本信息
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        framerate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        
        # 获取音频数据
        frames = wav_file.readframes(num_frames)
        
    # 向API发起请求
    content_data = {"audio_format": "wav", "raw_audio": frames, "rate": 16000}
    message = appbuilder.Message(content_data)
    # print(message)
    speech_result = asr.run(message).content['result'][0]
    print('语音识别结果：', speech_result)
    return speech_result
