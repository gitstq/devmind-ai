# -*- coding: utf-8 -*-
"""
代码复杂度分析器
"""
import math
from typing import Dict, List, Any


class ComplexityAnalyzer:
    """代码复杂度分析器"""
    
    def __init__(self):
        self.metrics = {}
    
    def analyze(self, parsed_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析所有文件的复杂度"""
        total_metrics = {
            "total_files": len(parsed_files),
            "total_lines": 0,
            "total_functions": 0,
            "total_classes": 0,
            "avg_file_complexity": 0.0,
            "files": [],
        }
        
        complexities = []
        
        for parsed in parsed_files:
            file_metrics = self._analyze_file(parsed)
            total_metrics["files"].append(file_metrics)
            total_metrics["total_lines"] += parsed.get("line_count", 0)
            
            structure = parsed.get("structure", {})
            total_metrics["total_functions"] += len(structure.get("functions", []))
            total_metrics["total_classes"] += len(structure.get("classes", []))
            
            complexities.append(file_metrics["complexity_score"])
        
        if complexities:
            total_metrics["avg_file_complexity"] = sum(complexities) / len(complexities)
        
        return total_metrics
    
    def _analyze_file(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """分析单个文件的复杂度"""
        content = parsed.get("content", "")
        structure = parsed.get("structure", {})
        lines = content.splitlines()
        
        # 基础指标
        line_count = len(lines)
        code_lines = len([l for l in lines if l.strip() and not l.strip().startswith("#")])
        comment_lines = len([l for l in lines if l.strip().startswith("#")])
        blank_lines = line_count - code_lines - comment_lines
        
        # 结构复杂度
        func_count = len(structure.get("functions", []))
        class_count = len(structure.get("classes", []))
        import_count = len(structure.get("imports", []))
        
        # 圈复杂度估算
        cyclomatic = self._estimate_cyclomatic(content)
        
        # 综合复杂度分数 (0-100)
        complexity_score = self._calculate_complexity_score(
            line_count, func_count, class_count, cyclomatic, import_count
        )
        
        return {
            "file_path": parsed.get("file_path", ""),
            "language": parsed.get("language", ""),
            "line_count": line_count,
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "blank_lines": blank_lines,
            "comment_ratio": comment_lines / line_count if line_count > 0 else 0,
            "function_count": func_count,
            "class_count": class_count,
            "import_count": import_count,
            "cyclomatic_complexity": cyclomatic,
            "complexity_score": complexity_score,
            "complexity_level": self._get_complexity_level(complexity_score),
        }
    
    def _estimate_cyclomatic(self, content: str) -> int:
        """估算圈复杂度"""
        complexity = 1  # 基础复杂度
        
        # 条件语句
        complexity += content.count("if ")
        complexity += content.count("elif ")
        complexity += content.count("else:")
        
        # 循环
        complexity += content.count("for ")
        complexity += content.count("while ")
        
        # 异常处理
        complexity += content.count("except")
        complexity += content.count("finally:")
        
        # 逻辑运算符
        complexity += content.count(" and ")
        complexity += content.count(" or ")
        
        # 三元表达式
        complexity += content.count("?")
        
        return complexity
    
    def _calculate_complexity_score(
        self, 
        lines: int, 
        funcs: int, 
        classes: int, 
        cyclomatic: int,
        imports: int
    ) -> float:
        """计算综合复杂度分数"""
        # 文件大小因子 (0-30)
        size_score = min(30, lines / 50)
        
        # 结构复杂度因子 (0-30)
        structure_score = min(30, (funcs * 3 + classes * 5) / 2)
        
        # 圈复杂度因子 (0-30)
        cyclo_score = min(30, cyclomatic / 3)
        
        # 依赖复杂度因子 (0-10)
        dep_score = min(10, imports / 2)
        
        total = size_score + structure_score + cyclo_score + dep_score
        return round(min(100, total), 2)
    
    def _get_complexity_level(self, score: float) -> str:
        """获取复杂度等级"""
        if score < 20:
            return "简单"
        elif score < 40:
            return "中等"
        elif score < 60:
            return "复杂"
        elif score < 80:
            return "很复杂"
        else:
            return "极复杂"
