from utils.asr import *
from utils.vlm import *
from utils.tts import *
from utils.camera import *
import cv2
import os
import time

def take_picture(PROMPT='帮我把图片中的文字提取出来'):
    if _recording:
        print("摄像头正在录制中，请先停止录制")
        # 播放welcome音频
        text_to_speech = TextToSpeech() # 创建 TextToSpeech 和 AudioPlayer 实例
        text_to_speech.synthesize_to_wav("摄像头正在录制中，请先停止录制", output_path="temp/please_stop_video.wav")
        AudioPlayer.play_wav('temp/please_stop_video.wav')
        return

    
    # 播放welcome音频
    text_to_speech = TextToSpeech() # 创建 TextToSpeech 和 AudioPlayer 实例
    text_to_speech.synthesize_to_wav("请将眼镜对着书本", output_path="temp/welcome.wav")
    AudioPlayer.play_wav('temp/welcome.wav')


    img_path = 'temp/vl_now.jpg'
    # 拍照
    top_view_shot(img_path)
    
    # 将图片输入给多模态视觉大模型
    n = 1
    while n < 5:
        try:
            print('    尝试第 {} 次访问多模态大模型'.format(n))
            result = qwen_vlm(PROMPT, img_path='temp/vl_now.jpg')
            print('    多模态大模型调用成功！')
            print("从图片中读取到的内容为：",result)
            break
        except Exception as e:
            # print('    多模态大模型返回数据结构错误，再尝试一次', e)
            # print(result)
            n += 1
    

    # 文字转语音
    text_to_speech.synthesize_to_wav(result, output_path="temp/book_content.wav")
    AudioPlayer.play_wav('temp/book_content.wav')

def top_view_shot(img_path='temp/vl_now.jpg'):
    # 确保temp目录存在
    os.makedirs(os.path.dirname(img_path), exist_ok=True)
    
    # 初始化摄像头
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("无法打开摄像头")
        return False
    
    try:
        # 等待0.5秒让摄像头稳定
        time.sleep(0.5)
        
        # 拍照
        ret, frame = cap.read()
        if not ret:
            print("无法获取图像")
            return False
            
        # 保存图片
        cv2.imwrite(img_path, frame)
        print(f"照片已保存到: {img_path}")
        return True
        
    finally:
        # 释放摄像头
        cap.release()