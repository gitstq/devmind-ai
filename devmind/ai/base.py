# -*- coding: utf-8 -*-
"""
AI后端抽象基类
"""
from abc import ABC, abstractmethod
from typing import Optional


class AIBackend(ABC):
    """AI后端抽象基类"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def generate_docstring(
        self, 
        code: str, 
        language: str,
        style: str = "google"
    ) -> str:
        """
        生成函数/类的文档字符串
        
        Args:
            code: 代码内容
            language: 编程语言
            style: 文档风格 (google, numpy, restdoc)
        
        Returns:
            生成的文档字符串
        """
        pass
    
    @abstractmethod
    def optimize_code(self, code: str, language: str) -> str:
        """
        提供代码优化建议
        
        Args:
            code: 代码内容
            language: 编程语言
        
        Returns:
            优化建议文本
        """
        pass
    
    @abstractmethod
    def explain_code(self, code: str, language: str) -> str:
        """
        解释代码功能
        
        Args:
            code: 代码内容
            language: 编程语言
        
        Returns:
            代码解释文本
        """
        pass
    
    def is_available(self) -> bool:
        """检查后端是否可用"""
        return True
