import pandas as pd
from . import call_gemini
from .executor import CodeExecutor

class DataCleanerAgent:
    """数据清洗与分析 Agent，协调流程编排"""

    def __init__(self):
        self.executor = CodeExecutor()

    def generate_prompt(self, df_head: str, columns: str, describe: str) -> str:
        """构建给 LLM 的系统提示词"""
        prompt = f"""
你现在是一个资深的 Python 数据分析师和 Pandas 专家。
你的任务是：基于提供的数据样本和结构，编写用于“清理”这些数据的 Pandas 代码。

【当前数据概况】
列名：{columns}
前5行数据样本：
{df_head}
基础统计特征：
{describe}

【你的任务与要求】
1. 分析数据中可能存在的脏数据：比如缺失值 (NaN)、格式错误的日期、异常的字符串、异常值等。
2. 编写一段干净、健壮的 Python Pandas 脚本来清洗这份数据。
3. 你的代码中，**原始数据已经被加载到名为 `df` 的变量中**。
4. 你的代码最后，**必须将清洗后的 DataFrame 赋值给一个名为 `cleaned_df` 的变量**。
5. 请只返回 Python 代码，用 ```python 开始，用 ``` 结束，不要加任何其他聊天废话，也不要自己写 import pd，或者读写文件。

【代码示例参考】
```python
# 1. 填充缺失值
df['age'].fillna(df['age'].mean(), inplace=True)
# 2. 去除前后空格
if 'name' in df.columns:
    df['name'] = df['name'].str.strip()
# 3. 将结果赋给约定好的变量
cleaned_df = df
```
请开始编写针对当前数据的清洗代码：
"""
        return prompt

    def run(self, csv_path: str) -> tuple[str, str]:
        """
        核心工作流
        :param csv_path: 待清洗的原始 CSV 路径
        :return: (清洗后保存的CSV路径, LLM生成的代码日志)
        """
        # 1. 探索数据
        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            return "", f"读取文件失败: {str(e)}"
            
        df_head = df.head(5).to_markdown()
        columns = ", ".join(df.columns.tolist())
        describe = df.describe().to_markdown()

        # 2. 构造 Prompt
        prompt = self.generate_prompt(df_head, columns, describe)

        # 3. 呼叫大模型获取代码
        print(">>> 正在请求大模型思考清洗方案并编写代码...")
        llm_response = call_gemini(prompt)

        # 4. 提取代码并执行
        code = self.executor.extract_python_code(llm_response)
        
        try:
            print(">>> 正在沙箱中执行 Agent 生成的代码...")
            cleaned_df = self.executor.execute_pandas_code(code, df)
            
            # 5. 保存结果
            output_path = csv_path.replace(".csv", "_cleaned.csv")
            cleaned_df.to_csv(output_path, index=False)
            print(f">>> 清洗成功，结果已保存至 {output_path}")
            
            return output_path, code
        except Exception as e:
            return "", f"执行失败:\n{str(e)}\n\nLLM 原始输出:\n{llm_response}"
