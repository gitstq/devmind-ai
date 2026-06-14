# -*- coding: utf-8 -*-
"""
文档生成器
"""
from pathlib import Path
from typing import Dict, List, Optional, Any

from jinja2 import Template

from ..ai.base import AIBackend


# 文档模板
GOOGLE_STYLE_TEMPLATE = """\"\"\"{{ description }}

{% if args %}
Args:
{% for arg in args %}
    {{ arg.name }} ({{ arg.type }}): {{ arg.description }}
{% endfor %}
{% endif %}

{% if returns %}
Returns:
    {{ returns.type }}: {{ returns.description }}
{% endif %}

{% if raises %}
Raises:
{% for exc in raises %}
    {{ exc.type }}: {{ exc.description }}
{% endfor %}
{% endif %}

{% if examples %}
Examples:
    {{ examples }}
{% endif %}
\"\"\""""

NUMPY_STYLE_TEMPLATE = """\"\"\"{{ description }}

{% if args %}
Parameters
----------
{% for arg in args %}
{{ arg.name }} : {{ arg.type }}
    {{ arg.description }}
{% endfor %}
{% endif %}

{% if returns %}
Returns
-------
{{ returns.type }}
    {{ returns.description }}
{% endif %}

{% if raises %}
Raises
------
{% for exc in raises %}
{{ exc.type }}
    {{ exc.description }}
{% endfor %}
{% endif %}
\"\"\""""

RESTDOC_STYLE_TEMPLATE = """\"\"\"{{ description }}

{% if args %}
{% for arg in args %}
:param {{ arg.name }}: {{ arg.description }}
:type {{ arg.name }}: {{ arg.type }}
{% endfor %}
{% endif %}

{% if returns %}
:return: {{ returns.description }}
:rtype: {{ returns.type }}
{% endif %}

{% if raises %}
{% for exc in raises %}
:raise {{ exc.type }}: {{ exc.description }}
{% endfor %}
{% endif %}
\"\"\""""


class DocGenerator:
    """文档生成器"""
    
    TEMPLATES = {
        "google": GOOGLE_STYLE_TEMPLATE,
        "numpy": NUMPY_STYLE_TEMPLATE,
        "restdoc": RESTDOC_STYLE_TEMPLATE,
    }
    
    def __init__(self, backend: Optional[AIBackend] = None, style: str = "google"):
        self.backend = backend
        self.style = style
        self.template = Template(self.TEMPLATES.get(style, GOOGLE_STYLE_TEMPLATE))
    
    def generate_for_file(self, file_path: Path) -> str:
        """为单个文件生成文档"""
        content = file_path.read_text(encoding="utf-8")
        language = self._detect_language(file_path)
        
        # 如果有AI后端，使用AI生成
        if self.backend and self.backend.is_available():
            return self.backend.generate_docstring(content, language, self.style)
        
        # 否则使用模板生成基础文档
        return self._generate_template_doc(content, language)
    
    def generate_for_project(self, project_path: Path, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """为整个项目生成文档"""
        if output_dir:
            output_path = Path(output_dir)
        else:
            output_path = project_path / "docs"
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        stats = {"files": 0, "docs": 0}
        
        # 遍历项目文件
        for file_path in project_path.rglob("*"):
            if file_path.is_file() and self._is_code_file(file_path):
                stats["files"] += 1
                
                try:
                    doc_content = self.generate_for_file(file_path)
                    
                    # 保存文档
                    rel_path = file_path.relative_to(project_path)
                    doc_file = output_path / f"{rel_path}.md"
                    doc_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(doc_file, "w", encoding="utf-8") as f:
                        f.write(f"# {file_path.name}\n\n")
                        f.write(f"**路径:** `{rel_path}`\n\n")
                        f.write("## 文档\n\n")
                        f.write(f"```\n{doc_content}\n```\n")
                    
                    stats["docs"] += 1
                except Exception as e:
                    print(f"生成文档失败 {file_path}: {e}")
        
        return stats
    
    def _generate_template_doc(self, content: str, language: str) -> str:
        """使用模板生成基础文档"""
        # 简单提取函数签名
        import re
        
        func_match = re.search(r"def\s+(\w+)\s*\(([^)]*)\)", content)
        if not func_match:
            return "# 未能识别函数定义"
        
        func_name = func_match.group(1)
        args_str = func_match.group(2)
        
        # 解析参数
        args = []
        if args_str.strip():
            for arg in args_str.split(","):
                arg = arg.strip()
                if arg and arg != "self":
                    args.append({
                        "name": arg.split(":")[0].strip(),
                        "type": "Any",
                        "description": "待补充",
                    })
        
        context = {
            "description": f"{func_name} 函数的功能说明（待补充）",
            "args": args,
            "returns": {"type": "Any", "description": "返回值说明（待补充）"},
            "raises": [],
            "examples": "",
        }
        
        return self.template.render(**context)
    
    def _detect_language(self, file_path: Path) -> str:
        """检测文件语言"""
        suffix = file_path.suffix.lower()
        mapping = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".go": "go",
            ".java": "java",
        }
        return mapping.get(suffix, "unknown")
    
    def _is_code_file(self, file_path: Path) -> bool:
        """检查是否为代码文件"""
        return file_path.suffix.lower() in (".py", ".js", ".ts", ".go", ".java")
