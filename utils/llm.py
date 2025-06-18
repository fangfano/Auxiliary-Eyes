import ast
from openai import OpenAI
from API_KEY import *

# 智能决策用
def llm_qwen(PROMPT='你好，你是谁？'):

    API_BASE = QWEN_URL
    API_KEY = QWEN_KEY
    API_MODEL = QWEN_MODEL

    for i in range(3):
    # 访问大模型API
        client = OpenAI(api_key=API_KEY, base_url=API_BASE)

        completion = client.chat.completions.create(
            model = API_MODEL,
            messages=[{"role": "user", "content": PROMPT}],
        )
        response_content = completion.choices[0].message.content.strip()
        print(f"[DEBUG] 原始响应内容:\n{response_content}")  # 打印原始内容
        cleaned_content = response_content.replace("```json", "").replace("```", "").strip()
        # print(f"[DEBUG] 清洗后内容:\n{cleaned_content}")    # 打印清洗后内容
        # print(type(cleaned_content))
        result = ast.literal_eval(cleaned_content)
        # result = json.loads(cleaned_content)
        if type(result) is list and result != []:
            break
        else:
            print("大模型返回结果错误,正在重新请求结果")
            
    return result

