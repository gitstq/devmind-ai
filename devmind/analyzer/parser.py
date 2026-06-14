# -*- coding: utf-8 -*-
"""
代码解析器
支持 Python, JavaScript, Go, Java
"""
import re
from pathlib import Path
from typing import Dict, List, Optional, Any


class CodeParser:
    """代码解析器"""
    
    # 语言映射
    LANGUAGE_MAP = {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".go": "go",
        ".java": "java",
    }
    
    # 忽略的文件模式
    IGNORE_PATTERNS = [
        r"__pycache__",
        r"\.pyc$",
        r"node_modules",
        r"\.git",
        r"venv",
        r"\.env",
        r"\.min\.js$",
        r"dist",
        r"build",
    ]
    
    def __init__(self):
        self.results = []
    
    def detect_language(self, file_path: Path) -> str:
        """检测文件语言"""
        suffix = file_path.suffix.lower()
        return self.LANGUAGE_MAP.get(suffix, "unknown")
    
    def should_ignore(self, path: Path) -> bool:
        """检查路径是否应该被忽略"""
        path_str = str(path)
        for pattern in self.IGNORE_PATTERNS:
            if re.search(pattern, path_str):
                return True
        return False
    
    def discover_files(self, root_path: Path, max_size_mb: int = 5) -> List[Path]:
        """发现所有可解析的文件"""
        files = []
        
        if root_path.is_file():
            if self.detect_language(root_path) != "unknown":
                files.append(root_path)
            return files
        
        for path in root_path.rglob("*"):
            if path.is_file() and not self.should_ignore(path):
                # 检查文件大小
                try:
                    size_mb = path.stat().st_size / (1024 * 1024)
                    if size_mb <= max_size_mb:
                        lang = self.detect_language(path)
                        if lang != "unknown":
                            files.append(path)
                except (OSError, PermissionError):
                    continue
        
        return sorted(files)
    
    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """解析单个文件"""
        language = self.detect_language(file_path)
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        
        if language == "python":
            structure = self._parse_python(content)
        elif language in ("javascript", "typescript"):
            structure = self._parse_javascript(content)
        elif language == "go":
            structure = self._parse_go(content)
        elif language == "java":
            structure = self._parse_java(content)
        else:
            structure = {"type": "unknown", "content": content}
        
        return {
            "file_path": str(file_path),
            "language": language,
            "content": content,
            "structure": structure,
            "line_count": len(content.splitlines()),
        }
    
    def parse_project(self, root_path: Path, max_depth: int = 3) -> Dict[str, Any]:
        """解析整个项目"""
        files = self.discover_files(root_path)
        
        project_structure = {
            "root": str(root_path),
            "files": [],
            "summary": {
                "total_files": len(files),
                "languages": {},
                "total_lines": 0,
            },
        }
        
        for file_path in files:
            parsed = self.parse_file(file_path)
            project_structure["files"].append(parsed)
            
            lang = parsed["language"]
            project_structure["summary"]["languages"][lang] = \
                project_structure["summary"]["languages"].get(lang, 0) + 1
            project_structure["summary"]["total_lines"] += parsed["line_count"]
        
        return project_structure
    
    def _parse_python(self, content: str) -> Dict[str, Any]:
        """解析Python代码结构"""
        structure = {
            "type": "python",
            "imports": [],
            "classes": [],
            "functions": [],
            "variables": [],
        }
        
        lines = content.splitlines()
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # 导入语句
            if re.match(r"^(import|from)\s+", stripped):
                structure["imports"].append({
                    "line": i + 1,
                    "content": stripped,
                })
            
            # 类定义
            class_match = re.match(r"^class\s+(\w+)(?:\(([^)]*)\))?:", stripped)
            if class_match:
                structure["classes"].append({
                    "name": class_match.group(1),
                    "line": i + 1,
                    "bases": class_match.group(2) or "",
                })
            
            # 函数定义
            func_match = re.match(r"^(?:async\s+)?def\s+(\w+)\s*\(([^)]*)\)", stripped)
            if func_match:
                structure["functions"].append({
                    "name": func_match.group(1),
                    "line": i + 1,
                    "args": func_match.group(2),
                    "async": stripped.startswith("async"),
                })
        
        return structure
    
    def _parse_javascript(self, content: str) -> Dict[str, Any]:
        """解析JavaScript/TypeScript代码结构"""
        structure = {
            "type": "javascript",
            "imports": [],
            "classes": [],
            "functions": [],
            "exports": [],
        }
        
        lines = content.splitlines()
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # 导入/导出
            if re.match(r"^(import|export)\s+", stripped):
                structure["imports"].append({
                    "line": i + 1,
                    "content": stripped,
                })
            
            # 类定义
            class_match = re.match(r"^class\s+(\w+)(?:\s+extends\s+(\w+))?", stripped)
            if class_match:
                structure["classes"].append({
                    "name": class_match.group(1),
                    "line": i + 1,
                    "extends": class_match.group(2) or None,
                })
            
            # 函数定义（多种方式）
            func_patterns = [
                r"^(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)",
                r"^(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(([^)]*)\)\s*=>",
                r"^(?:const|let|var)\s+(\w+)\s*=\s*function\s*\(([^)]*)\)",
            ]
            
            for pattern in func_patterns:
                func_match = re.match(pattern, stripped)
                if func_match:
                    structure["functions"].append({
                        "name": func_match.group(1),
                        "line": i + 1,
                        "args": func_match.group(2),
                    })
                    break
        
        return structure
    
    def _parse_go(self, content: str) -> Dict[str, Any]:
        """解析Go代码结构"""
        structure = {
            "type": "go",
            "package": "",
            "imports": [],
            "structs": [],
            "functions": [],
            "interfaces": [],
        }
        
        lines = content.splitlines()
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # 包声明
            pkg_match = re.match(r"^package\s+(\w+)", stripped)
            if pkg_match:
                structure["package"] = pkg_match.group(1)
            
            # 导入
            if stripped.startswith("import "):
                structure["imports"].append({
                    "line": i + 1,
                    "content": stripped,
                })
            
            # 结构体
            struct_match = re.match(r"^type\s+(\w+)\s+struct", stripped)
            if struct_match:
                structure["structs"].append({
                    "name": struct_match.group(1),
                    "line": i + 1,
                })
            
            # 接口
            interface_match = re.match(r"^type\s+(\w+)\s+interface", stripped)
            if interface_match:
                structure["interfaces"].append({
                    "name": interface_match.group(1),
                    "line": i + 1,
                })
            
            # 函数
            func_match = re.match(r"^func\s+(?:\([^)]+\)\s+)?(\w+)\s*\(([^)]*)\)", stripped)
            if func_match:
                structure["functions"].append({
                    "name": func_match.group(1),
                    "line": i + 1,
                    "args": func_match.group(2),
                })
        
        return structure
    
    def _parse_java(self, content: str) -> Dict[str, Any]:
        """解析Java代码结构"""
        structure = {
            "type": "java",
            "package": "",
            "imports": [],
            "classes": [],
            "methods": [],
        }
        
        lines = content.splitlines()
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # 包声明
            pkg_match = re.match(r"^package\s+([\w.]+);", stripped)
            if pkg_match:
                structure["package"] = pkg_match.group(1)
            
            # 导入
            import_match = re.match(r"^import\s+([\w.]+);", stripped)
            if import_match:
                structure["imports"].append({
                    "line": i + 1,
                    "content": import_match.group(1),
                })
            
            # 类定义
            class_match = re.match(
                r"^(?:public\s+)?(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w,\s]+))?",
                stripped,
            )
            if class_match:
                structure["classes"].append({
                    "name": class_match.group(1),
                    "line": i + 1,
                    "extends": class_match.group(2),
                    "implements": class_match.group(3),
                })
            
            # 方法定义
            method_match = re.match(
                r"^(?:public|private|protected)?\s*(?:static\s+)?(?:\w+(?:<[^>]+>)?\s+)?(\w+)\s*\(([^)]*)\)",
                stripped,
            )
            if method_match and not stripped.startswith("if") and not stripped.startswith("while"):
                structure["methods"].append({
                    "name": method_match.group(1),
                    "line": i + 1,
                    "args": method_match.group(2),
                })
        
        return structure
