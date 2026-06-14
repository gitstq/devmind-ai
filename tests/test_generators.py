# -*- coding: utf-8 -*-
"""
生成器测试
"""
import tempfile
from pathlib import Path

import pytest

from devmind.generators.docs import DocGenerator
from devmind.generators.mindmap import MindMapGenerator


class TestDocGenerator:
    """测试文档生成器"""
    
    def setup_method(self):
        self.generator = DocGenerator(style="google")
    
    def test_generate_template_doc(self):
        """测试模板文档生成"""
        code = '''
def greet(name):
    return f"Hello, {name}!"
'''
        doc = self.generator._generate_template_doc(code, "python")
        
        assert "greet" in doc
        assert "Args:" in doc
        assert "name" in doc
    
    def test_detect_language(self):
        """测试语言检测"""
        assert self.generator._detect_language(Path("test.py")) == "python"
        assert self.generator._detect_language(Path("test.js")) == "javascript"
    
    def test_is_code_file(self):
        """测试代码文件判断"""
        assert self.generator._is_code_file(Path("test.py"))
        assert not self.generator._is_code_file(Path("test.txt"))


class TestMindMapGenerator:
    """测试思维导图生成器"""
    
    def setup_method(self):
        self.generator = MindMapGenerator(format="mermaid")
    
    def test_generate_mermaid(self):
        """测试Mermaid格式生成"""
        structure = {
            "file_path": "/test/main.py",
            "language": "python",
            "structure": {
                "type": "python",
                "imports": [
                    {"line": 1, "content": "import os"},
                ],
                "classes": [
                    {"name": "TestClass", "line": 3},
                ],
                "functions": [
                    {"name": "main", "line": 6, "args": ""},
                ],
            },
        }
        
        result = self.generator.generate(structure)
        
        assert "mermaid" in result
        assert "main.py" in result
        assert "TestClass" in result
        assert "main()" in result
    
    def test_generate_markdown(self):
        """测试Markdown格式生成"""
        generator = MindMapGenerator(format="markdown")
        
        structure = {
            "file_path": "/test/main.py",
            "language": "python",
            "structure": {
                "type": "python",
                "functions": [
                    {"name": "main", "line": 1},
                ],
            },
        }
        
        result = generator.generate(structure)
        
        assert "# 代码结构思维导图" in result
        assert "main.py" in result
        assert "main()" in result
    
    def test_generate_project_mindmap(self):
        """测试项目级思维导图"""
        structure = {
            "root": "/test/project",
            "files": [
                {
                    "file_path": "/test/project/main.py",
                    "language": "python",
                    "structure": {
                        "functions": [{"name": "main"}],
                    },
                },
                {
                    "file_path": "/test/project/utils.js",
                    "language": "javascript",
                    "structure": {
                        "functions": [{"name": "helper"}],
                    },
                },
            ],
        }
        
        result = self.generator.generate(structure)
        
        assert "project" in result
        assert "python" in result
        assert "javascript" in result
