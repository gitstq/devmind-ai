# -*- coding: utf-8 -*-
"""
复杂度分析器测试
"""
import tempfile
from pathlib import Path

import pytest

from devmind.analyzer.parser import CodeParser
from devmind.analyzer.metrics import ComplexityAnalyzer


class TestComplexityAnalyzer:
    """测试复杂度分析器"""
    
    def setup_method(self):
        self.analyzer = ComplexityAnalyzer()
        self.parser = CodeParser()
    
    def test_simple_file(self):
        """测试简单文件分析"""
        code = '''
def simple():
    return 42
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = Path(f.name)
        
        try:
            parsed = self.parser.parse_file(temp_path)
            metrics = self.analyzer._analyze_file(parsed)
            
            assert metrics["line_count"] == 3
            assert metrics["function_count"] == 1
            assert metrics["complexity_score"] < 30
            assert metrics["complexity_level"] == "简单"
        finally:
            temp_path.unlink()
    
    def test_complex_file(self):
        """测试复杂文件分析"""
        code = '''
def complex_function(data):
    result = []
    for item in data:
        if item > 0:
            if item % 2 == 0:
                result.append(item * 2)
            else:
                result.append(item * 3)
        elif item < 0:
            try:
                result.append(abs(item))
            except Exception:
                pass
        else:
            while len(result) < 10:
                result.append(0)
    return result

class DataProcessor:
    def process(self, data):
        return complex_function(data)
    
    def validate(self, data):
        return all(x is not None for x in data)
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = Path(f.name)
        
        try:
            parsed = self.parser.parse_file(temp_path)
            metrics = self.analyzer._analyze_file(parsed)
            
            assert metrics["function_count"] == 3
            assert metrics["class_count"] == 1
            assert metrics["cyclomatic_complexity"] > 5
            assert metrics["complexity_score"] > 10
        finally:
            temp_path.unlink()
    
    def test_analyze_multiple_files(self):
        """测试多文件分析"""
        files = []
        
        try:
            for i in range(3):
                code = f'''
def func_{i}():
    return {i}
'''
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(code)
                    files.append(Path(f.name))
            
            parsed_files = [self.parser.parse_file(f) for f in files]
            metrics = self.analyzer.analyze(parsed_files)
            
            assert metrics["total_files"] == 3
            assert metrics["total_functions"] == 3
            assert "avg_file_complexity" in metrics
        finally:
            for f in files:
                f.unlink()
