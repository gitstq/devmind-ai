# -*- coding: utf-8 -*-
"""
Ollama本地模型后端
"""
import json
from typing import Optional

import requests

from .base import AIBackend


class OllamaBackend(AIBackend):
    """Ollama本地模型后端"""
    
    def __init__(self, host: str = "http://localhost:11434", model: str = "codellama"):
        super().__init__(name="Ollama")
        self.host = host.rstrip("/")
        self.model = model
        self._api_url = f"{self.host}/api/generate"
    
    def _generate(self, prompt: str, system: Optional[str] = None) -> str:
        """调用Ollama生成文本"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        
        if system:
            payload["system"] = system
        
        try:
            response = requests.post(
                self._api_url,
                json=payload,
                timeout=120,
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except requests.exceptions.ConnectionError:
            return "[错误] 无法连接到Ollama服务，请确保Ollama已启动"
        except requests.exceptions.Timeout:
            return "[错误] 请求超时，请检查模型是否正在加载"
        except Exception as e:
            return f"[错误] 请求失败: {str(e)}"
    
    def generate_docstring(self, code: str, language: str, style: str = "google") -> str:
        """生成文档字符串"""
        system_prompt = f"""你是一个专业的代码文档生成助手。请为给定的{language}代码生成{style}风格的文档字符串。
只返回文档字符串内容，不要包含其他解释。"""
        
        prompt = f"""请为以下{language}代码生成{style}风格的文档字符串：

```{language}
{code}
```

要求：
1. 包含函数/类的功能描述
2. 包含所有参数说明
3. 包含返回值说明
4. 包含可能的异常说明（如有）
5. 使用{language}注释语法

只返回文档字符串："""
        
        return self._generate(prompt, system=system_prompt)
    
    def optimize_code(self, code: str, language: str) -> str:
        """提供代码优化建议"""
        system_prompt = f"""你是一个专业的代码优化专家。请分析给定的{language}代码，提供具体的优化建议。
建议应包括性能、可读性、安全性等方面。"""
        
        prompt = f"""请分析以下{language}代码，提供优化建议：

```{language}
{code}
```

请按以下格式输出：
1. 代码问题分析
2. 具体优化建议
3. 优化后的代码示例（如有）"""
        
        return self._generate(prompt, system=system_prompt)
    
    def explain_code(self, code: str, language: str) -> str:
        """解释代码功能"""
        system_prompt = f"""你是一个专业的代码解释专家。请用简洁清晰的语言解释{language}代码的功能和逻辑。"""
        
        prompt = f"""请解释以下{language}代码的功能：

```{language}
{code}
```

要求：
1. 说明整体功能
2. 解释关键逻辑
3. 指出重要函数/类的作用"""
        
        return self._generate(prompt, system=system_prompt)
    
    def is_available(self) -> bool:
        """检查Ollama服务是否可用"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
