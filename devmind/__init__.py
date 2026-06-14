"""
DevMind AI - 智能开发者思维助手

基于AI的代码分析、智能注释生成、代码优化建议与思维导图生成工具。
支持本地模型(Ollama)和云端API(OpenAI/Claude)多后端。

版本: 1.0.0
作者: DevMind Team
许可证: MIT
"""

__version__ = "1.0.0"
__author__ = "DevMind Team"
__license__ = "MIT"

from .analyzer.parser import CodeParser
from .analyzer.metrics import ComplexityAnalyzer
from .ai.base import AIBackend
from .generators.docs import DocGenerator
from .generators.mindmap import MindMapGenerator

__all__ = [
    "CodeParser",
    "ComplexityAnalyzer", 
    "AIBackend",
    "DocGenerator",
    "MindMapGenerator",
]
