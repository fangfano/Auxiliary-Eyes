
import time
import cv2
import numpy as np
from PIL import Image
from PIL import ImageFont, ImageDraw

import json
# 导入中文字体，指定字号
font = ImageFont.truetype('asset/SimHei.ttf', 26)

from API_KEY import *

# # 系统提示词
# SYSTEM_PROMPT = ''''''

# Yi-Vision调用函数
from openai import OpenAI
import base64
def qwen_vlm(PROMPT='帮我把图片中的文字提取出来', img_path='temp/vl_now.jpg'):
    
    client = OpenAI(
        api_key= QWEN_KEY,
        base_url= QWEN_URL,
    )
    
    # 编码为base64数据
    with open(img_path, 'rb') as image_file:
        image = 'data:image/jpeg;base64,' + base64.b64encode(image_file.read()).decode('utf-8')
    
    # 向大模型发起请求
    completion = client.chat.completions.create(
      model= QWEN_MODEL,
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": PROMPT
            },
            {
              "type": "image_url",
              "image_url": {
                "url": image
              }
            }
          ]
        },
      ]
    )
    
    # 解析大模型返回结果
    response_content = completion.choices[0].message.content.strip()
    print(f"[DEBUG] 原始响应内容:\n{response_content}")  # 打印原始内容
    # cleaned_content = response_content.replace("```json", "").replace("```", "").strip()
    # # print(f"[DEBUG] 清洗后内容:\n{cleaned_content}")    # 打印清洗后内容
    # result = json.loads(cleaned_content)
    # print('大模型调用成功！')
    return response_content
