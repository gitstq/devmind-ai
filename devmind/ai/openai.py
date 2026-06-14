# -*- coding: utf-8 -*-
"""
OpenAI API后端
"""
from typing import Optional

import requests

from .base import AIBackend


class OpenAIBackend(AIBackend):
    """OpenAI API后端（兼容OpenAI格式）"""
    
    def __init__(
        self, 
        api_key: str, 
        model: str = "gpt-4",
        base_url: Optional[str] = None
    ):
        super().__init__(name="OpenAI")
        self.api_key = api_key
        self.model = model
        self.base_url = (base_url or "https://api.openai.com/v1").rstrip("/")
        self._chat_url = f"{self.base_url}/chat/completions"
    
    def _generate(self, prompt: str, system: Optional[str] = None) -> str:
        """调用OpenAI API生成文本"""
        if not self.api_key:
            return "[错误] 未设置API密钥"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 2000,
        }
        
        try:
            response = requests.post(
                self._chat_url,
                headers=headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except requests.exceptions.ConnectionError:
            return "[错误] 无法连接到API服务器"
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                return "[错误] API密钥无效"
            elif response.status_code == 429:
                return "[错误] 请求过于频繁，请稍后再试"
            return f"[错误] API请求失败: {response.status_code}"
        except Exception as e:
            return f"[错误] 请求失败: {str(e)}"
    
    def generate_docstring(self, code: str, language: str, style: str = "google") -> str:
        """生成文档字符串"""
        system_prompt = f"""You are a professional code documentation assistant. 
Generate {style}-style docstrings for the given {language} code.
Return only the docstring content without any explanation."""
        
        prompt = f"""Generate a {style}-style docstring for this {language} code:

```{language}
{code}
```

Requirements:
1. Include function/class description
2. Include all parameter descriptions
3. Include return value description
4. Include exception descriptions (if any)
5. Use {language} comment syntax

Return only the docstring:"""
        
        return self._generate(prompt, system=system_prompt)
    
    def optimize_code(self, code: str, language: str) -> str:
        """提供代码优化建议"""
        system_prompt = f"""You are a professional code optimization expert. 
Analyze the given {language} code and provide specific optimization suggestions.
Cover performance, readability, and security aspects."""
        
        prompt = f"""Analyze this {language} code and provide optimization suggestions:

```{language}
{code}
```

Please output in this format:
1. Code issue analysis
2. Specific optimization suggestions
3. Optimized code example (if applicable)"""
        
        return self._generate(prompt, system=system_prompt)
    
    def explain_code(self, code: str, language: str) -> str:
        """解释代码功能"""
        system_prompt = f"""You are a professional code explanation expert. 
Explain {language} code functionality in clear, concise language."""
        
        prompt = f"""Explain the functionality of this {language} code:

```{language}
{code}
```

Requirements:
1. Explain overall functionality
2. Explain key logic
3. Point out important functions/classes"""
        
        return self._generate(prompt, system=system_prompt)
    
    def is_available(self) -> bool:
        """检查API是否可用"""
        if not self.api_key:
            return False
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(
                f"{self.base_url}/models",
                headers=headers,
                timeout=10,
            )
            return response.status_code == 200
        except:
            return False
