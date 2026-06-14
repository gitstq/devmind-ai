# 🧠 DevMind AI

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/AI-Ollama%20%7C%20OpenAI-orange" alt="AI Backend">
</p>

<p align="center">
  <b>Intelligent Developer Mind Assistant</b> —— AI-powered code analysis, smart documentation, mindmap generation & optimization tool
</p>

---

## 🎉 Introduction

DevMind AI is an intelligent assistant designed for developers:

- 🔍 **Deep Code Analysis** —— Auto-parse project structure, calculate complexity metrics
- 📝 **Smart Documentation** —— AI-generated docstrings following best practices
- 🗺️ **Mindmap Visualization** —— Convert code structure to Mermaid/Markdown mindmaps
- ⚡ **Code Optimization** —— Identify bottlenecks and suggest refactoring

### 🌟 Why DevMind AI?

| Feature | DevMind AI | Others |
|---------|-----------|--------|
| Local Execution | ✅ Fully Local | ❌ Cloud-dependent |
| Multi-language | ✅ Python/JS/Go/Java | ⚠️ Limited |
| Mindmap | ✅ Auto-generate | ❌ Not supported |
| Complexity Analysis | ✅ Built-in | ⚠️ Plugin needed |
| AI Backends | ✅ Ollama/OpenAI | ⚠️ Single backend |

---

## ✨ Core Features

### 📊 Code Analysis (`analyze`)

```bash
devmind analyze ./my-project --format html --output report.html
```

### 📝 Smart Docs (`doc`)

Supports multiple documentation styles:

- **Google Style**
- **NumPy Style**
- **reStructuredText**

```bash
devmind doc ./src/main.py --style google
```

### 🗺️ Mindmap (`mindmap`)

```bash
devmind mindmap ./src --format mermaid --output architecture.md
```

### ⚡ Optimization (`optimize`)

```bash
devmind optimize ./src/bottleneck.py --suggest
```

---

## 🚀 Quick Start

### Installation

```bash
pip install devmind-ai
```

### Initialize Config

```bash
devmind init
```

### Basic Usage

```bash
# Analyze code
devmind analyze ./my-project

# Generate docs
devmind doc ./my-project/src

# Generate mindmap
devmind mindmap ./my-project/src
```

---

## 📖 AI Backend Configuration

### Using Ollama (Recommended)

```yaml
ai:
  backend: ollama
  ollama:
    host: http://localhost:11434
    model: codellama
```

### Using OpenAI API

```yaml
ai:
  backend: openai
  openai:
    api_key: "sk-your-api-key"
    model: gpt-4
```

---

## 📄 License

[MIT License](./LICENSE)

---

<p align="center">
  Made with ❤️ by DevMind Team
</p>
