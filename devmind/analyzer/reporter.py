# -*- coding: utf-8 -*-
"""
分析报告生成器
"""
import json
from typing import Dict, List, Any

from rich.table import Table
from rich.console import Console


class AnalysisReporter:
    """分析报告生成器"""
    
    def __init__(self):
        self.console = Console()
    
    def generate(self, results: List[Dict], metrics: Dict, format: str = "text") -> str:
        """生成报告"""
        if format == "json":
            return self._generate_json(results, metrics)
        elif format == "html":
            return self._generate_html(results, metrics)
        else:
            return self._generate_text(results, metrics)
    
    def _generate_text(self, results: List[Dict], metrics: Dict) -> str:
        """生成文本报告"""
        lines = []
        lines.append("=" * 60)
        lines.append("代码分析报告")
        lines.append("=" * 60)
        lines.append("")
        
        # 概览
        lines.append("📊 概览")
        lines.append("-" * 40)
        lines.append(f"总文件数: {metrics['total_files']}")
        lines.append(f"总行数: {metrics['total_lines']}")
        lines.append(f"总函数数: {metrics['total_functions']}")
        lines.append(f"总类数: {metrics['total_classes']}")
        lines.append(f"平均复杂度: {metrics['avg_file_complexity']:.2f}")
        lines.append("")
        
        # 文件详情
        lines.append("📁 文件详情")
        lines.append("-" * 40)
        
        for file_metric in metrics.get("files", []):
            lines.append(f"\n文件: {file_metric['file_path']}")
            lines.append(f"  语言: {file_metric['language']}")
            lines.append(f"  行数: {file_metric['line_count']} (代码: {file_metric['code_lines']}, 注释: {file_metric['comment_lines']})")
            lines.append(f"  函数: {file_metric['function_count']}, 类: {file_metric['class_count']}")
            lines.append(f"  圈复杂度: {file_metric['cyclomatic_complexity']}")
            lines.append(f"  综合复杂度: {file_metric['complexity_score']} ({file_metric['complexity_level']})")
            
            # 复杂度警告
            if file_metric['complexity_score'] >= 60:
                lines.append(f"  ⚠️  警告: 该文件复杂度较高，建议重构")
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def _generate_json(self, results: List[Dict], metrics: Dict) -> str:
        """生成JSON报告"""
        report = {
            "summary": {
                "total_files": metrics["total_files"],
                "total_lines": metrics["total_lines"],
                "total_functions": metrics["total_functions"],
                "total_classes": metrics["total_classes"],
                "avg_complexity": metrics["avg_file_complexity"],
            },
            "files": metrics.get("files", []),
        }
        return json.dumps(report, ensure_ascii=False, indent=2)
    
    def _generate_html(self, results: List[Dict], metrics: Dict) -> str:
        """生成HTML报告"""
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>DevMind AI - 代码分析报告</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }
        .card { background: white; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .metric-card { background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; }
        .metric-value { font-size: 2em; font-weight: bold; color: #667eea; }
        .metric-label { color: #666; margin-top: 5px; }
        .file-item { border-left: 4px solid #667eea; padding: 15px; margin-bottom: 15px; background: #f8f9fa; border-radius: 0 8px 8px 0; }
        .warning { border-left-color: #ff6b6b; background: #fff5f5; }
        .complexity-high { color: #ff6b6b; font-weight: bold; }
        .complexity-medium { color: #feca57; font-weight: bold; }
        .complexity-low { color: #48dbfb; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #f8f9fa; font-weight: 600; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 DevMind AI</h1>
        <p>代码分析报告</p>
    </div>
"""
        
        # 概览
        html += f"""
    <div class="card">
        <h2>📊 概览</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">{metrics['total_files']}</div>
                <div class="metric-label">总文件数</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics['total_lines']}</div>
                <div class="metric-label">总行数</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics['total_functions']}</div>
                <div class="metric-label">总函数数</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics['avg_file_complexity']:.1f}</div>
                <div class="metric-label">平均复杂度</div>
            </div>
        </div>
    </div>
"""
        
        # 文件详情
        html += """
    <div class="card">
        <h2>📁 文件详情</h2>
        <table>
            <tr>
                <th>文件</th>
                <th>语言</th>
                <th>行数</th>
                <th>函数</th>
                <th>类</th>
                <th>复杂度</th>
                <th>等级</th>
            </tr>
"""
        
        for file_metric in metrics.get("files", []):
            complexity_class = "complexity-low"
            if file_metric['complexity_score'] >= 60:
                complexity_class = "complexity-high"
            elif file_metric['complexity_score'] >= 40:
                complexity_class = "complexity-medium"
            
            html += f"""
            <tr>
                <td>{file_metric['file_path']}</td>
                <td>{file_metric['language']}</td>
                <td>{file_metric['line_count']}</td>
                <td>{file_metric['function_count']}</td>
                <td>{file_metric['class_count']}</td>
                <td class="{complexity_class}">{file_metric['complexity_score']}</td>
                <td>{file_metric['complexity_level']}</td>
            </tr>
"""
        
        html += """
        </table>
    </div>
</body>
</html>
"""
        
        return html
