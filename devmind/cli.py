#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevMind AI - 命令行入口
"""
import os
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .analyzer.parser import CodeParser
from .analyzer.metrics import ComplexityAnalyzer
from .analyzer.reporter import AnalysisReporter
from .ai.ollama import OllamaBackend
from .ai.openai import OpenAIBackend
from .generators.docs import DocGenerator
from .generators.mindmap import MindMapGenerator
from .utils.config import Config

console = Console()


def print_banner():
    """打印欢迎横幅"""
    banner = Text()
    banner.append("🧠 ", style="bold cyan")
    banner.append("DevMind AI", style="bold bright_cyan")
    banner.append(" - 智能开发者思维助手\n", style="dim")
    banner.append("v1.0.0 ", style="dim")
    banner.append("| ", style="dim")
    banner.append("MIT License", style="dim")
    console.print(Panel(banner, border_style="cyan"))


def get_ai_backend(config: Config):
    """根据配置获取AI后端"""
    backend_type = config.get("ai.backend", "ollama")
    
    if backend_type == "ollama":
        return OllamaBackend(
            host=config.get("ai.ollama.host", "http://localhost:11434"),
            model=config.get("ai.ollama.model", "codellama"),
        )
    elif backend_type == "openai":
        return OpenAIBackend(
            api_key=config.get("ai.openai.api_key", ""),
            model=config.get("ai.openai.model", "gpt-4"),
            base_url=config.get("ai.openai.base_url", None),
        )
    else:
        raise click.ClickException(f"不支持的AI后端: {backend_type}")


@click.group()
@click.option("--config", "-c", type=click.Path(), help="配置文件路径")
@click.option("--verbose", "-v", is_flag=True, help="详细输出模式")
@click.pass_context
def cli(ctx, config, verbose):
    """DevMind AI - 智能开发者思维助手"""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    
    # 加载配置
    config_path = config or os.path.expanduser("~/.devmind/config.yaml")
    ctx.obj["config"] = Config(config_path)
    
    if verbose:
        console.print(f"[dim]配置加载: {config_path}[/dim]")


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="输出报告路径")
@click.option("--format", "-f", type=click.Choice(["text", "json", "html"]), default="text")
@click.pass_context
def analyze(ctx, path, output, format):
    """分析代码结构与复杂度"""
    print_banner()
    
    target_path = Path(path)
    config = ctx.obj["config"]
    
    console.print(f"[bold]正在分析:[/bold] {target_path}")
    
    # 解析代码
    parser = CodeParser()
    files = parser.discover_files(target_path)
    
    with console.status("[bold green]解析代码中..."):
        results = []
        for file_path in files:
            try:
                result = parser.parse_file(file_path)
                results.append(result)
            except Exception as e:
                if ctx.obj["verbose"]:
                    console.print(f"[yellow]警告: 无法解析 {file_path}: {e}[/yellow]")
    
    # 复杂度分析
    analyzer = ComplexityAnalyzer()
    metrics = analyzer.analyze(results)
    
    # 生成报告
    reporter = AnalysisReporter()
    report = reporter.generate(results, metrics, format=format)
    
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(report)
        console.print(f"[green]报告已保存: {output}[/green]")
    else:
        console.print(report)
    
    console.print(f"\n[bold]分析完成![/bold] 共分析 {len(files)} 个文件")


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--style", "-s", 
              type=click.Choice(["google", "numpy", "restdoc"]), 
              default="google",
              help="文档风格")
@click.option("--output", "-o", type=click.Path(), help="输出目录")
@click.option("--dry-run", is_flag=True, help="预览模式，不写入文件")
@click.pass_context
def doc(ctx, path, style, output, dry_run):
    """自动生成代码文档"""
    print_banner()
    
    target_path = Path(path)
    config = ctx.obj["config"]
    
    console.print(f"[bold]正在生成文档:[/bold] {target_path}")
    console.print(f"[dim]文档风格: {style}[/dim]")
    
    # 获取AI后端
    try:
        backend = get_ai_backend(config)
        console.print(f"[dim]AI后端: {backend.name}[/dim]")
    except Exception as e:
        console.print(f"[yellow]警告: AI后端初始化失败 ({e})，将使用模板生成[/yellow]")
        backend = None
    
    # 生成文档
    generator = DocGenerator(backend=backend, style=style)
    
    with console.status("[bold green]生成文档中..."):
        if target_path.is_file():
            docs = generator.generate_for_file(target_path)
            if dry_run:
                console.print(Panel(docs, title="预览", border_style="blue"))
            else:
                output_path = output or target_path.with_suffix(".md")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(docs)
                console.print(f"[green]文档已保存: {output_path}[/green]")
        else:
            stats = generator.generate_for_project(target_path, output)
            if dry_run:
                console.print("[yellow]项目级文档预览模式暂不支持[/yellow]")
            else:
                console.print(f"[green]项目文档生成完成![/green]")
                console.print(f"  处理文件: {stats['files']}")
                console.print(f"  生成文档: {stats['docs']}")


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--format", "-f", 
              type=click.Choice(["mermaid", "markdown", "json"]), 
              default="mermaid",
              help="输出格式")
@click.option("--output", "-o", type=click.Path(), help="输出文件路径")
@click.option("--depth", "-d", type=int, default=3, help="最大深度")
@click.pass_context
def mindmap(ctx, path, format, output, depth):
    """生成代码思维导图"""
    print_banner()
    
    target_path = Path(path)
    
    console.print(f"[bold]正在生成思维导图:[/bold] {target_path}")
    console.print(f"[dim]格式: {format} | 深度: {depth}[/dim]")
    
    # 解析代码
    parser = CodeParser()
    
    with console.status("[bold green]解析代码结构..."):
        if target_path.is_file():
            structure = parser.parse_file(target_path)
        else:
            structure = parser.parse_project(target_path, max_depth=depth)
    
    # 生成思维导图
    generator = MindMapGenerator(format=format)
    mindmap_content = generator.generate(structure, max_depth=depth)
    
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(mindmap_content)
        console.print(f"[green]思维导图已保存: {output}[/green]")
    else:
        console.print(Panel(mindmap_content, title="思维导图", border_style="green"))
    
    console.print("\n[bold]提示:[/bold] 将Mermaid内容粘贴到支持Mermaid的编辑器中查看图形")


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--suggest", is_flag=True, help="生成优化建议")
@click.option("--apply", is_flag=True, help="应用优化（谨慎使用）")
@click.pass_context
def optimize(ctx, path, suggest, apply):
    """代码优化建议"""
    print_banner()
    
    target_path = Path(path)
    config = ctx.obj["config"]
    
    console.print(f"[bold]正在分析优化空间:[/bold] {target_path}")
    
    # 获取AI后端
    try:
        backend = get_ai_backend(config)
    except Exception as e:
        console.print(f"[red]错误: AI后端初始化失败: {e}[/red]")
        return
    
    # 解析并优化
    parser = CodeParser()
    
    with console.status("[bold green]AI分析中..."):
        if target_path.is_file():
            code = target_path.read_text(encoding="utf-8")
            suggestions = backend.optimize_code(code, language=parser.detect_language(target_path))
            
            console.print(Panel(suggestions, title="优化建议", border_style="yellow"))
            
            if apply:
                console.print("[yellow]注意: 自动应用功能需要手动确认[/yellow]")
        else:
            console.print("[yellow]项目级优化建议暂不支持，请指定单个文件[/yellow]")


@cli.command()
def init():
    """初始化配置文件"""
    config_dir = Path.home() / ".devmind"
    config_file = config_dir / "config.yaml"
    
    if config_file.exists():
        if not click.confirm("配置文件已存在，是否覆盖?"):
            return
    
    config_dir.mkdir(parents=True, exist_ok=True)
    
    default_config = """# DevMind AI 配置文件

# AI后端配置
ai:
  # 后端类型: ollama | openai
  backend: ollama
  
  # Ollama配置（本地模型）
  ollama:
    host: http://localhost:11434
    model: codellama
  
  # OpenAI配置（云端API）
  openai:
    api_key: ""  # 请填写你的API密钥
    model: gpt-4
    base_url: null  # 可选，用于兼容API

# 分析配置
analysis:
  # 忽略的文件模式
  ignore_patterns:
    - "*.pyc"
    - "__pycache__"
    - "node_modules"
    - ".git"
    - "venv"
    - ".env"
  
  # 最大文件大小 (MB)
  max_file_size: 5

# 文档生成配置
documentation:
  # 默认文档风格
  default_style: google
  # 包含类型注解
  include_types: true
  # 包含示例代码
  include_examples: true

# 思维导图配置
mindmap:
  # 默认输出格式
  default_format: mermaid
  # 最大深度
  max_depth: 3
"""
    
    with open(config_file, "w", encoding="utf-8") as f:
        f.write(default_config)
    
    console.print(f"[green]配置文件已创建: {config_file}[/green]")
    console.print("[dim]请编辑配置文件以设置你的AI后端[/dim]")


@cli.command()
def version():
    """显示版本信息"""
    print_banner()
    console.print(f"Python: {sys.version}")
    console.print(f"平台: {sys.platform}")


def main():
    """主入口"""
    cli()


if __name__ == "__main__":
    main()
