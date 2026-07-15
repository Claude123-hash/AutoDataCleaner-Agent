import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

# 读取环境变量
load_dotenv()

# 初始化 Gemini 客户端
# 你需要在项目根目录创建一个 .env 文件，并在里面写入 GEMINI_API_KEY=你的密钥
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("WARNING: 未找到 GEMINI_API_KEY 环境变量。请配置后再试。")

def call_gemini(prompt: str) -> str:
    """调用 Gemini 模型生成代码"""
    try:
        model = genai.GenerativeModel('gemini-3.1-flash-lite')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: LLM 调用失败 - {str(e)}"
