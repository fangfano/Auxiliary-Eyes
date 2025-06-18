import cv2
import numpy as np
import threading
import os
from datetime import datetime

# 全局变量用于控制录制状态
_recording = False
_camera_thread = None

def _record_video(filename):
    global _recording
    
    # 创建video目录（如果不存在）
    os.makedirs("video", exist_ok=True)
    
    # 初始化摄像头
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("无法打开摄像头")
        _recording = False
        return
        
    # 获取视频参数
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 20.0
    
    # 创建视频写入器
    output_path = os.path.join("video", f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    
    try:
        while _recording:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 写入视频帧
            out.write(frame)
            
    finally:
        # 释放资源
        cap.release()
        out.release()
        _recording = False


def start_camera(filename = "公园散步"):
    global _recording, _camera_thread
    
    # 检查是否已经在录制
    if _recording:
        print("摄像头已经在录制中")
        return False
        
    # 设置录制状态并启动录制线程
    _recording = True
    _camera_thread = threading.Thread(target=_record_video, args=(filename,))
    _camera_thread.start()
    return True

def stop_camera():
    global _recording, _camera_thread
    
    # 检查是否正在录制
    if not _recording:
        print("摄像头未在录制中")
        return False
        
    # 停止录制
    _recording = False
    if _camera_thread:
        _camera_thread.join()  # 等待录制线程结束
        _camera_thread = None
        
    return True