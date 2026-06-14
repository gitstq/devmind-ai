# -*- coding: utf-8 -*-
"""
代码解析器测试
"""
import tempfile
from pathlib import Path

import pytest

from devmind.analyzer.parser import CodeParser


class TestCodeParser:
    """测试代码解析器"""
    
    def setup_method(self):
        self.parser = CodeParser()
    
    def test_detect_language_python(self):
        """测试Python语言检测"""
        assert self.parser.detect_language(Path("test.py")) == "python"
    
    def test_detect_language_javascript(self):
        """测试JavaScript语言检测"""
        assert self.parser.detect_language(Path("test.js")) == "javascript"
    
    def test_detect_language_unknown(self):
        """测试未知语言检测"""
        assert self.parser.detect_language(Path("test.txt")) == "unknown"
    
    def test_should_ignore(self):
        """测试忽略规则"""
        assert self.parser.should_ignore(Path("__pycache__/test.py"))
        assert not self.parser.should_ignore(Path("src/main.py"))
    
    def test_parse_python(self):
        """测试Python代码解析"""
        code = '''
import os
from pathlib import Path

class TestClass:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, {self.name}!"

def helper():
    pass
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = Path(f.name)
        
        try:
            result = self.parser.parse_file(temp_path)
            assert result["language"] == "python"
            assert result["line_count"] > 0
            
            structure = result["structure"]
            assert len(structure["classes"]) == 1
            assert structure["classes"][0]["name"] == "TestClass"
            assert len(structure["functions"]) == 3
            assert len(structure["imports"]) == 2
        finally:
            temp_path.unlink()
    
    def test_parse_javascript(self):
        """测试JavaScript代码解析"""
        code = '''
import React from 'react';

class MyComponent extends React.Component {
    render() {
        return <div>Hello</div>;
    }
}

function helper() {
    return 42;
}

const arrow = (x) => x * 2;
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            temp_path = Path(f.name)
        
        try:
            result = self.parser.parse_file(temp_path)
            assert result["language"] == "javascript"
            
            structure = result["structure"]
            assert len(structure["classes"]) == 1
            assert len(structure["functions"]) >= 2
        finally:
            temp_path.unlink()
    
    def test_discover_files(self):
        """测试文件发现"""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            
            # 创建测试文件
            (root / "main.py").write_text("print('hello')")
            (root / "utils.py").write_text("def helper(): pass")
            (root / "__pycache__").mkdir()
            (root / "__pycache__" / "cache.pyc").write_text("")
            
            files = self.parser.discover_files(root)
            assert len(files) == 2
            
            file_names = [f.name for f in files]
            assert "main.py" in file_names
            assert "utils.py" in file_names
