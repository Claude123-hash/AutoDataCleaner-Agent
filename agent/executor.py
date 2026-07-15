import re
import pandas as pd

class CodeExecutor:
    """安全的本地代码沙箱执行器 (Demo 用)"""
    
    @staticmethod
    def extract_python_code(llm_response: str) -> str:
        """从 LLM 的回复中提取 python 代码块"""
        # 使用正则匹配 ```python ... ```
        pattern = r"```python(.*?)```"
        matches = re.findall(pattern, llm_response, re.DOTALL)
        if matches:
            return matches[0].strip()
        
        # 如果 LLM 没加 markdown 代码块，则假设整段都是代码
        return llm_response.strip()

    @staticmethod
    def execute_pandas_code(code: str, df: pd.DataFrame) -> pd.DataFrame:
        """
        在受限的作用域内执行 Pandas 代码。
        期望代码中存在名为 `cleaned_df` 的变量。
        """
        # 简单安全拦截：阻止常见恶意操作
        forbidden_keywords = ["os.system", "subprocess", "open(", "rm ", "shutil"]
        for kw in forbidden_keywords:
            if kw in code:
                raise ValueError(f"警告：检测到不安全的关键词或操作 '{kw}'。")

        # 准备沙箱局部作用域
        local_scope = {
            "pd": pd,
            "df": df.copy()  # 传入原始数据的副本
        }

        print("====== 准备执行 Agent 生成的代码 ======")
        print(code)
        print("=======================================")

        try:
            # 执行代码
            exec(code, {}, local_scope)
            
            # 尝试获取处理后的 DataFrame
            if "cleaned_df" in local_scope:
                return local_scope["cleaned_df"]
            elif "df" in local_scope:
                return local_scope["df"]
            else:
                raise ValueError("代码执行完毕，但在沙箱中未找到名为 'cleaned_df' 的变量。")
                
        except Exception as e:
            raise RuntimeError(f"Agent 代码执行过程中抛出异常: {str(e)}\n\n错误代码内容:\n{code}")
