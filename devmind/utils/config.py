# -*- coding: utf-8 -*-
"""
配置管理模块
"""
import os
from pathlib import Path
from typing import Any, Optional

import yaml


class Config:
    """配置管理类"""
    
    def __init__(self, config_path: Optional[str] = None):
        self._config = {}
        self._config_path = config_path
        
        if config_path and Path(config_path).exists():
            self.load(config_path)
        else:
            self._load_defaults()
    
    def load(self, path: str) -> None:
        """从文件加载配置"""
        with open(path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f) or {}
    
    def save(self, path: Optional[str] = None) -> None:
        """保存配置到文件"""
        save_path = path or self._config_path
        if not save_path:
            raise ValueError("未指定配置文件路径")
        
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            yaml.dump(self._config, f, allow_unicode=True, default_flow_style=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项（支持点号路径）"""
        keys = key.split(".")
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """设置配置项（支持点号路径）"""
        keys = key.split(".")
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def _load_defaults(self) -> None:
        """加载默认配置"""
        self._config = {
            "ai": {
                "backend": "ollama",
                "ollama": {
                    "host": "http://localhost:11434",
                    "model": "codellama",
                },
                "openai": {
                    "api_key": "",
                    "model": "gpt-4",
                    "base_url": None,
                },
            },
            "analysis": {
                "ignore_patterns": [
                    "*.pyc", "__pycache__", "node_modules",
                    ".git", "venv", ".env", "*.min.js",
                ],
                "max_file_size": 5,
            },
            "documentation": {
                "default_style": "google",
                "include_types": True,
                "include_examples": True,
            },
            "mindmap": {
                "default_format": "mermaid",
                "max_depth": 3,
            },
        }
    
    def to_dict(self) -> dict:
        """返回配置字典"""
        return self._config.copy()
