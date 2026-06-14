# 🧠 DevMind AI

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/AI-Ollama%20%7C%20OpenAI-orange" alt="AI Backend">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey" alt="Platform">
</p>

<p align="center">
  <b>智能开发者思维助手</b> —— 基于AI的代码分析、智能注释生成、思维导图与优化建议工具
</p>

<p align="center">
  <a href="#-快速开始">快速开始</a> •
  <a href="#-核心特性">核心特性</a> •
  <a href="#-详细使用指南">使用指南</a> •
  <a href="#-安装">安装</a> •
  <a href="#-贡献指南">贡献</a>
</p>

---

## 🎉 项目介绍

DevMind AI 是一款专为开发者设计的智能助手工具，它能够：

- 🔍 **深度代码分析** —— 自动解析项目结构，计算复杂度指标
- 📝 **智能文档生成** —— 基于AI自动生成符合规范的文档字符串
- 🗺️ **思维导图可视化** —— 将代码结构转为Mermaid/Markdown思维导图
- ⚡ **代码优化建议** —— 识别性能瓶颈，提供重构方案

与 GitHub Copilot 等工具不同，DevMind AI **支持纯本地运行**，你的代码永远不会离开自己的电脑，完美保护隐私。

### 🌟 为什么选择 DevMind AI？

| 特性 | DevMind AI | 其他工具 |
|------|-----------|---------|
| 本地运行 | ✅ 完全本地 | ❌ 云端依赖 |
| 多语言支持 | ✅ Python/JS/Go/Java | ⚠️ 有限支持 |
| 思维导图 | ✅ 自动生成 | ❌ 不支持 |
| 复杂度分析 | ✅ 内置 | ⚠️ 需插件 |
| 多AI后端 | ✅ Ollama/OpenAI | ⚠️ 单一后端 |
| 中文优化 | ✅ 原生支持 | ⚠️ 一般 |

---

## ✨ 核心特性

### 📊 代码分析 (`analyze`)

自动发现项目中的代码文件，解析函数、类、导入关系，生成复杂度报告：

- 文件级复杂度评分 (0-100)
- 圈复杂度估算
- 代码/注释/空行统计
- 多格式报告输出 (文本/JSON/HTML)

```bash
devmind analyze ./my-project --format html --output report.html
```

### 📝 智能文档 (`doc`)

为代码自动生成专业文档字符串，支持多种风格：

- **Google Style** —— Google Python风格指南
- **NumPy Style** —— NumPy/SciPy文档规范
- **reStructuredText** —— Sphinx文档标准

```bash
# 为单个文件生成文档
devmind doc ./src/main.py --style google

# 为整个项目生成文档
devmind doc ./src --output ./docs
```

### 🗺️ 思维导图 (`mindmap`)

将代码结构可视化为思维导图：

- **Mermaid** 格式 —— 支持GitHub、Notion等渲染
- **Markdown** 格式 —— 通用文档格式
- **JSON** 格式 —— 程序化使用

```bash
devmind mindmap ./src --format mermaid --output architecture.md
```

### ⚡ 代码优化 (`optimize`)

AI驱动的代码优化建议：

- 性能瓶颈识别
- 可读性改进
- 安全性检查
- 重构方案生成

```bash
devmind optimize ./src/bottleneck.py --suggest
```

---

## 🚀 快速开始

### 安装

```bash
# 使用 pip 安装
pip install devmind-ai

# 或从源码安装
git clone https://github.com/gitstq/devmind-ai.git
cd devmind-ai
pip install -e ".[all]"
```

### 初始化配置

```bash
# 创建默认配置文件
devmind init

# 编辑 ~/.devmind/config.yaml 配置AI后端
```

### 基本使用

```bash
# 1. 分析代码
devmind analyze ./my-project

# 2. 生成文档
devmind doc ./my-project/src --style google

# 3. 生成思维导图
devmind mindmap ./my-project/src --format mermaid

# 4. 获取优化建议
devmind optimize ./my-project/src/main.py
```

---

## 📖 详细使用指南

### 配置AI后端

#### 使用 Ollama（推荐，完全本地）

```yaml
# ~/.devmind/config.yaml
ai:
  backend: ollama
  ollama:
    host: http://localhost:11434
    model: codellama
```

```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 拉取代码模型
ollama pull codellama
```

#### 使用 OpenAI API

```yaml
# ~/.devmind/config.yaml
ai:
  backend: openai
  openai:
    api_key: "sk-your-api-key"
    model: gpt-4
```

### 分析命令详解

```bash
# 基础分析
devmind analyze ./project

# 输出JSON格式
devmind analyze ./project --format json

# 生成HTML报告
devmind analyze ./project --format html --output report.html

# 详细模式
devmind analyze ./project --verbose
```

### 文档生成详解

```bash
# Google风格（默认）
devmind doc ./src/main.py

# NumPy风格
devmind doc ./src/main.py --style numpy

# 批量生成项目文档
devmind doc ./src --output ./docs --style google

# 预览模式（不写入文件）
devmind doc ./src/main.py --dry-run
```

### 思维导图详解

```bash
# Mermaid格式（默认）
devmind mindmap ./src

# Markdown格式
devmind mindmap ./src --format markdown

# 限制深度
devmind mindmap ./src --depth 2

# 保存到文件
devmind mindmap ./src --output mindmap.md
```

---

## 💡 设计思路与迭代规划

### 架构设计

```
DevMind AI
├── CLI Layer (Click + Rich)
│   ├── analyze  → 代码分析命令
│   ├── doc      → 文档生成命令
│   ├── mindmap  → 思维导图命令
│   └── optimize → 优化建议命令
├── Analyzer Engine
│   ├── Parser   → 多语言代码解析
│   ├── Metrics  → 复杂度计算
│   └── Reporter → 报告生成
├── AI Backend
│   ├── Ollama   → 本地模型
│   └── OpenAI   → 云端API
└── Generators
    ├── Docs     → 文档生成
    └── MindMap  → 思维导图生成
```

### 迭代路线图

- [x] v1.0.0 — 核心功能发布
  - [x] 多语言代码解析 (Python/JS/Go/Java)
  - [x] 复杂度分析
  - [x] AI文档生成
  - [x] 思维导图生成
  - [x] Ollama/OpenAI双后端
- [ ] v1.1.0 — 增强分析
  - [ ] 依赖关系图生成
  - [ ] 代码相似度检测
  - [ ] 安全漏洞扫描
- [ ] v1.2.0 — 更多语言
  - [ ] Rust/C++支持
  - [ ] TypeScript深度解析
  - [ ] 配置文件解析
- [ ] v2.0.0 — 智能升级
  - [ ] 多Agent协作
  - [ ] 自动重构执行
  - [ ] IDE插件支持

---

## 📦 打包与部署指南

### 开发环境

```bash
# 克隆仓库
git clone https://github.com/gitstq/devmind-ai.git
cd devmind-ai

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装开发依赖
pip install -e ".[dev,all]"

# 运行测试
make test

# 代码检查
make lint

# 格式化代码
make format
```

### 构建发布

```bash
# 清理构建产物
make clean

# 构建包
make build

# 上传到PyPI
make upload
```

### 系统要求

- **Python**: 3.9 或更高版本
- **操作系统**: Linux, macOS, Windows
- **内存**: 最低 512MB，推荐 2GB+
- **磁盘**: 100MB 安装空间

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！请参考 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解详情。

### 快速贡献步骤

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 行为准则

- 尊重所有参与者
- 接受建设性批评
- 关注社区利益
- 表示同理心

---

## 📄 开源协议说明

本项目采用 [MIT License](./LICENSE) 开源协议。

```
MIT License

Copyright (c) 2026 DevMind Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 致谢

感谢以下开源项目的支持：

- [Click](https://click.palletsprojects.com/) — 优雅的CLI框架
- [Rich](https://rich.readthedocs.io/) — 终端美化库
- [Tree-sitter](https://tree-sitter.github.io/) — 代码解析引擎
- [Jinja2](https://jinja.palletsprojects.com/) — 模板引擎

---

<p align="center">
  Made with ❤️ by DevMind Team
</p>

<p align="center">
  <a href="https://github.com/gitstq/devmind-ai">GitHub</a> •
  <a href="https://github.com/gitstq/devmind-ai/issues">Issues</a> •
  <a href="https://github.com/gitstq/devmind-ai/discussions">Discussions</a>
</p>
