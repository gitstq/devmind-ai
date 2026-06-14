# -*- coding: utf-8 -*-
"""
AI后端模块
"""
from .base import AIBackend
from .ollama import OllamaBackend
from .openai import OpenAIBackend

__all__ = ["AIBackend", "OllamaBackend", "OpenAIBackend"]
