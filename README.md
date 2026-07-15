# Auto Data-Cleaner Agent 🤖📊

## 🛠️ 技术栈
*   **前端**: 原生 HTML5 / CSS3 / JavaScript
*   **后端框架**: FastAPI, Uvicorn
*   **数据处理**: Pandas, NumPy, Tabulate
*   **大模型接口**: Google Generative AI SDK
*   **代码安全**: 内置 Python 沙箱 `exec` 执行拦截

## 🚀 快速启动指南

### 1. 环境准备
确保你的电脑上安装了 **Python 3.10+。
```bash
# 进入项目目录
cd AutoDataCleaner-Agent

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API Key
在项目根目录复制 `.env.example` 并重命名为 `.env`，填入你的 API Key：
```ini
GEMINI_API_KEY=AIzaSy...这里填入你的真实Key...
```

### 3. 运行服务
```bash
python app.py
# 服务启动后将运行在 http://127.0.0.1:8000
```

### 4. 体验与演示
1. 打开浏览器访问网页主页：[http://127.0.0.1:8000](http://127.0.0.1:8000)
2. 将项目根目录下的测试脏数据 `test_dirty_data.csv` 拖拽到上传区域。
3. 点击 **“开始智能清洗”**，稍等片刻，即可看到 Agent 实时生成的 Pandas 清洗代码，并可以直接下载清洗好的干净 CSV 文件.


## 📂 核心代码架构说明
*   `app.py`: FastAPI 主入口，挂载前端页面并暴露数据处理 API。
*   `index.html`: 前端单页面。
*   `agent/cleaner.py`: 核心 Agent 提示词工程所在地，负责分析数据特征并向 LLM 请求代码。
*   `agent/executor.py`: 本地代码安全沙箱，防止 LLM 执行危险代码。
*   `test_dirty_data.csv`: 预设的测试数据集（包含负数年龄、错误日期格式、缺失值等，用于演示效果）。
