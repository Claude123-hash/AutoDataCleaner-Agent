import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from pydantic import BaseModel
from agent.cleaner import DataCleanerAgent

app = FastAPI(
    title="Auto Data-Cleaner Agent API",
    description="利用大模型自动编写 Pandas 脚本并执行的智能数据清洗工作流",
    version="1.0.0"
)

# 确保存放临时文件的目录存在
TEMP_DIR = "temp_data"
os.makedirs(TEMP_DIR, exist_ok=True)

class ProcessResponse(BaseModel):
    status: str
    message: str
    cleaned_file_url: str | None = None
    llm_code: str | None = None

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_frontend():
    """返回基于 Glassmorphism 设计的高级 Web 前端页面"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return HTMLResponse(content=f"<h1>UI 加载失败</h1><p>请确保 index.html 存在于项目根目录下。错误：{str(e)}</p>", status_code=500)

@app.post("/upload_and_clean/", response_model=ProcessResponse, tags=["Agent 工作流"])
async def upload_and_clean(file: UploadFile = File(...)):
    """
    上传一份包含脏数据的 CSV 文件，Agent 会自动分析并清洗数据，返回清洗日志和新的文件下载地址。
    """
    if not file.filename.endswith('.csv'):
        return JSONResponse(status_code=400, content={"status": "error", "message": "目前仅支持 CSV 格式的文件"})
        
    # 1. 保存上传的文件
    file_path = os.path.join(TEMP_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 2. 调用 Agent
    agent = DataCleanerAgent()
    output_path, result_or_code = agent.run(file_path)
    
    # 3. 处理结果
    if output_path:
        # 成功
        download_url = f"/download/{os.path.basename(output_path)}"
        return ProcessResponse(
            status="success",
            message="数据清洗完成",
            cleaned_file_url=download_url,
            llm_code=result_or_code
        )
    else:
        # 失败
        return JSONResponse(
            status_code=500, 
            content={
                "status": "error", 
                "message": "清洗任务执行失败", 
                "llm_code": result_or_code
            }
        )

@app.get("/download/{filename}", tags=["文件管理"])
async def download_file(filename: str):
    """
    下载清洗后的结果文件
    """
    file_path = os.path.join(TEMP_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='text/csv')
    return JSONResponse(status_code=404, content={"message": "文件不存在"})

if __name__ == "__main__":
    import uvicorn
    # 为了方便运行，也可以直接在此文件通过 python app.py 启动
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
