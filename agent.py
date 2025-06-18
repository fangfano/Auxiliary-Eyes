# 导入常用函数
from utils.asr import *             # 录音+语音识别
from utils.llm import *             # 大语言模型API
from utils.camera import *          # 摄像头
from utils.dir import *            # GPIO、夹爪
from utils.vlm_move import *        # 多模态大模型识别图像，夹爪抓取并移动物体
from utils.agent import *           # 智能体Agent编排
from utils.tts import *
import playsound


# 播放welcome音频
say_hello()


def agent_play():
    '''
    主函数，语音控制智目智能体编排动作
    '''
    # 输入指令
    start_record_ok = 'k'
    if start_record_ok == 'k':
        playsound.playsound("./temp/beep.mp3")  # 播放提示音  
        # record(DURATION=10)   # 录音
        result = record_until_silence(
            output_filename="temp/speech_record.wav",
            noise_sample_time=0.5,    # 采样环境噪音的时间(秒)
            max_silence_wait=5.0,     # 最大等待时间(秒)
            silence_duration=2.0      # 静音持续时间(秒)
        ) 
        if result["status"] == False:
            text_to_speech.synthesize_to_wav(result["msg"], output_path='temp/record_error.wav')
            AudioPlayer.play_wav('temp/record_error.wav')
            return
        
        order = speech_recognition() # 语音识别
    else:
        print('无指令，退出')
        return
    
    text_to_speech.synthesize_to_wav("收到,开启智能决策", output_path='temp/Start_smart_orchestration.wav')
    # print('播放语音合成音频')
    AudioPlayer.play_wav('temp/Start_smart_orchestration.wav')

    # 智能体Agent编排动作
    agent_plan_output = agent_plan(order)
    print('智能决策动作如下:', agent_plan_output)
    # text_to_speech.synthesize_to_wav("动作编排完成,开始执行", output_path='temp/Finish_smart_orchestration.wav')
    # AudioPlayer.play_wav('temp/Finish_smart_orchestration.wav')

    for each in agent_plan_output: # 运行智能体规划编排的每个函数
        print('开始执行动作', each)
        eval(each)
    # text_to_speech.synthesize_to_wav("任务已完成", output_path='temp/task_finished.wav')
    AudioPlayer.play_wav('temp/task_finished.wav')
