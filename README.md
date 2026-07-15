# Auto Data-Cleaner Agent 🤖📊

> 这是一个专为“AI产品开发/AI辅助工具”岗位设计的高含金量实习作品 Demo。

## 🌟 项目亮点 (为什么这个项目能证明你的能力？)

1. **真实切中业务痛点**：数据清洗是算法工程师和分析师最耗时的环节。本项目将这一“重复性、低效环节”彻底自动化，完美契合“工作流优化”的岗位职责。
2. **AI Agent 的深度实践 (Code Interpreter 思维)**：这不是简单的“调用 LLM 陪聊”，而是基于数据特征（Head、Describe）构建 Prompt，让 LLM 充当“数据分析师” **动态编写 Pandas Python 脚本**，并在受限沙箱中自动执行，输出结果。展现了你对 Agent 工作流的深刻理解。
3. **工程化与框架能力**：采用 **FastAPI** 现代后端框架，利用其自动生成的 OpenAPI UI 进行优雅展示。代码结构清晰（分为路由层、Agent 调度层、代码执行沙箱层），体现了良好的“代码规范”。

## 🛠️ 技术栈
*   **后端框架**: FastAPI, Uvicorn
*   **数据处理**: Pandas
*   **大模型接口**: Google Gemini Pro (可通过配置 `.env` 切换)
*   **安全与执行**: 内置 Python 沙箱 `exec` 执行隔离

## 🚀 快速启动指南

### 1. 环境准备
确保你的电脑上安装了 Python 3.9+。
```bash
# 进入项目目录
cd "D:\WUDownloadCache\实习\agent项目"

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API Key
在项目根目录复制 `.env.example` 为 `.env`，填入你的 Gemini API Key：
```ini
GEMINI_API_KEY=AIzaSy...这里填入你的真实Key...
```

### 3. 运行服务
```bash
python app.py
# 或者使用 uvicorn
# uvicorn app:app --reload
```

### 4. 体验 Demo (面向面试官)
1. 服务启动后，打开浏览器访问自动生成的 API 交互界面：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
2. 展开 `POST /upload_and_clean/` 接口，点击 `Try it out`。
3. 在 `file` 字段上传本项目根目录下提供的 `test_dirty_data.csv`。
   *(你打开这个 CSV 会发现它充满了空值、负数年龄、错误邮箱格式和错误日期)*
4. 点击 `Execute`，观察后端的控制台打印信息。
5. Agent 会自动探索数据，写出精准的清洗代码，你将在 Response body 中看到清洗日志，并拿到 `cleaned_file_url` 去下载干干净净的数据文件！

## 📂 核心代码架构说明
*   `app.py`: FastAPI 的 API 入口，负责接收文件流并返回 JSON 响应。
*   `agent/cleaner.py`: 核心提示词工程（Prompt Engineering）所在地，负责组装数据特征交给大模型。
*   `agent/executor.py`: 本地代码沙箱，拦截危险函数调用（如 `os.system`），执行 Pandas 代码并将结果从局部作用域中提取返回。
