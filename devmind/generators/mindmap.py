# -*- coding: utf-8 -*-
"""
思维导图生成器
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional


class MindMapGenerator:
    """思维导图生成器"""
    
    def __init__(self, format: str = "mermaid"):
        self.format = format
    
    def generate(self, structure: Dict[str, Any], max_depth: int = 3) -> str:
        """生成思维导图"""
        if self.format == "mermaid":
            return self._generate_mermaid(structure, max_depth)
        elif self.format == "markdown":
            return self._generate_markdown(structure, max_depth)
        elif self.format == "json":
            return self._generate_json(structure, max_depth)
        else:
            return self._generate_mermaid(structure, max_depth)
    
    def _generate_mermaid(self, structure: Dict[str, Any], max_depth: int) -> str:
        """生成Mermaid格式思维导图"""
        lines = ["```mermaid", "mindmap"]
        
        if "root" in structure:
            # 项目级思维导图
            root_name = Path(structure["root"]).name
            lines.append(f"  root(({root_name}))")
            
            # 按语言分组
            languages = {}
            for file_info in structure.get("files", []):
                lang = file_info.get("language", "unknown")
                if lang not in languages:
                    languages[lang] = []
                languages[lang].append(file_info)
            
            for lang, files in languages.items():
                lines.append(f"    {lang}")
                for file_info in files[:10]:  # 限制数量
                    file_name = Path(file_info["file_path"]).name
                    lines.append(f"      {file_name}")
                    
                    # 添加结构信息
                    file_structure = file_info.get("structure", {})
                    for func in file_structure.get("functions", [])[:3]:
                        lines.append(f"        {func['name']}()")
                    for cls in file_structure.get("classes", [])[:3]:
                        lines.append(f"        {cls['name']}")
        else:
            # 文件级思维导图
            file_path = structure.get("file_path", "unknown")
            file_name = Path(file_path).name
            lines.append(f"  root(({file_name}))")
            
            file_structure = structure.get("structure", {})
            
            # 导入
            imports = file_structure.get("imports", [])
            if imports:
                lines.append("    导入")
                for imp in imports[:5]:
                    lines.append(f"      {imp['content'][:30]}")
            
            # 类
            classes = file_structure.get("classes", [])
            if classes:
                lines.append("    类")
                for cls in classes[:5]:
                    lines.append(f"      {cls['name']}")
            
            # 函数
            functions = file_structure.get("functions", [])
            if functions:
                lines.append("    函数")
                for func in functions[:5]:
                    lines.append(f"      {func['name']}()")
        
        lines.append("```")
        return "\n".join(lines)
    
    def _generate_markdown(self, structure: Dict[str, Any], max_depth: int) -> str:
        """生成Markdown格式思维导图"""
        lines = ["# 代码结构思维导图", ""]
        
        if "root" in structure:
            root_name = Path(structure["root"]).name
            lines.append(f"## 项目: {root_name}")
            lines.append("")
            
            languages = {}
            for file_info in structure.get("files", []):
                lang = file_info.get("language", "unknown")
                if lang not in languages:
                    languages[lang] = []
                languages[lang].append(file_info)
            
            for lang, files in languages.items():
                lines.append(f"### {lang}")
                for file_info in files:
                    file_name = Path(file_info["file_path"]).name
                    lines.append(f"- **{file_name}**")
                    
                    file_structure = file_info.get("structure", {})
                    for func in file_structure.get("functions", [])[:3]:
                        lines.append(f"  - `{func['name']}()`")
                    for cls in file_structure.get("classes", [])[:3]:
                        lines.append(f"  - `class {cls['name']}`")
                lines.append("")
        else:
            file_path = structure.get("file_path", "unknown")
            lines.append(f"## 文件: {Path(file_path).name}")
            lines.append("")
            
            file_structure = structure.get("structure", {})
            
            if file_structure.get("imports"):
                lines.append("### 导入")
                for imp in file_structure["imports"]:
                    lines.append(f"- `{imp['content']}`")
                lines.append("")
            
            if file_structure.get("classes"):
                lines.append("### 类")
                for cls in file_structure["classes"]:
                    lines.append(f"- **{cls['name']}**")
                lines.append("")
            
            if file_structure.get("functions"):
                lines.append("### 函数")
                for func in file_structure["functions"]:
                    lines.append(f"- `{func['name']}()`")
                lines.append("")
        
        return "\n".join(lines)
    
    def _generate_json(self, structure: Dict[str, Any], max_depth: int) -> str:
        """生成JSON格式"""
        mindmap_data = {
            "type": "mindmap",
            "format": "json",
            "data": structure,
        }
        return json.dumps(mindmap_data, ensure_ascii=False, indent=2)
