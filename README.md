# 盲人辅助眼镜
这是一个为盲人提供视觉感知的辅助眼镜，生活中存在很多物品上面没有盲文标记（例如：药品盒、普通书本），为盲人带来了一定的困扰。因此就有了这个项目，想法来自于一位中国山东青岛的李沐恩小朋友，我帮助她实现这个小发明。

![demo](https://github.com/user-attachments/assets/7f7e11ac-3667-495b-89fa-8c63eaf47803)

---

## 演示视频

1.功能一：语音唤醒
https://github.com/user-attachments/assets/2b8d6953-a47d-4a82-a298-1db5c9824462

2.功能二：识别物体
https://github.com/user-attachments/assets/ccc98382-3fe4-4f7d-9c6f-133d5c94a3b0

3.功能三：录制视频
https://github.com/user-attachments/assets/0b37baf9-54fa-4428-bd4a-c0138240033c


---

## 硬件设备清单
1.OrangePi 3B 4G
购买链接：

https://e.tb.cn/h.hbw4XoGaOIyQ6hm?tk=v3gxVIzAiv7

![orangepi_3b](https://github.com/user-attachments/assets/1b19d306-2f6b-4a37-9b31-b393a6710ffb)


2.可架在眼镜上的摄像头
购买链接：

https://e.tb.cn/h.haocogLEb9bhMoB?tk=MlXNVqHS9NB

![yanjing](https://github.com/user-attachments/assets/8c268fbe-3c77-4eb8-9ff9-2c0f61d7e9b9)


3.USB有线小音响

购买链接：

https://e.tb.cn/h.hcZaRRi4oIQvx6r?tk=2ccrVtWi5wN

![USByingxiang](https://github.com/user-attachments/assets/ce2526e6-21b1-49a0-9a5d-5d0656be702a)


---

## 快速使用方法
1.项目根目录中的requirements.txt中的包可能不全，自行根据实际情况安装

``git clone https://github.com/fangfano/Auxiliary-Eyes.git``  

``pip install -r requirements.txt``

2.修改API_KEY.py中的key，请前往 百度智能云 和 通义千问 注册获取，有免费额度

`` 百度智能云key  :  ``

``APPBUILDER_TOKEN = "*****************************"``

`` 通义千问key  :`` 

``QWEN_KEY = "*****************************"``

3.到项目根目录启动项目

``python start.py``

4.使用唤醒词唤醒

对着麦克风说“hello hello”

等待音响出现“滴”的一声，表示唤醒成功

5.说说你想让它干什么

目前支持的功能有：

5.1 识别面前的物品或者文字

    语音指令为：“请问这是什么”

5.2 开始录制视频

    语音指令为：“请录制一个公园散步的视频”

5.3 停止录制视频

    语音指令为：“请停止视频录制”


5.4 开始录制视频

    语音指令为：“请打开视频保存的文件夹”




---


