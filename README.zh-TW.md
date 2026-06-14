# 🧠 DevMind AI

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/AI-Ollama%20%7C%20OpenAI-orange" alt="AI Backend">
</p>

<p align="center">
  <b>智能開發者思維助手</b> —— 基於AI的代碼分析、智能註釋生成、思維導圖與優化建議工具
</p>

---

## 🎉 項目介紹

DevMind AI 是一款專為開發者設計的智能助手工具：

- 🔍 **深度代碼分析** —— 自動解析項目結構，計算複雜度指標
- 📝 **智能文檔生成** —— 基於AI自動生成符合規範的文檔字符串
- 🗺️ **思維導圖可視化** —— 將代碼結構轉為Mermaid/Markdown思維導圖
- ⚡ **代碼優化建議** —— 識別性能瓶頸，提供重構方案

### 🌟 核心優勢

| 特性 | DevMind AI | 其他工具 |
|------|-----------|---------|
| 本地運行 | ✅ 完全本地 | ❌ 雲端依賴 |
| 多語言支持 | ✅ Python/JS/Go/Java | ⚠️ 有限支持 |
| 思維導圖 | ✅ 自動生成 | ❌ 不支持 |
| 複雜度分析 | ✅ 內置 | ⚠️ 需插件 |
| 多AI後端 | ✅ Ollama/OpenAI | ⚠️ 單一後端 |

---

## ✨ 核心特性

### 📊 代碼分析 (`analyze`)

自動發現項目中的代碼文件，解析函數、類、導入關係：

```bash
devmind analyze ./my-project --format html --output report.html
```

### 📝 智能文檔 (`doc`)

支持多種文檔風格：

- **Google Style** —— Google Python風格指南
- **NumPy Style** —— NumPy/SciPy文檔規範
- **reStructuredText** —— Sphinx文檔標準

```bash
devmind doc ./src/main.py --style google
```

### 🗺️ 思維導圖 (`mindmap`)

```bash
devmind mindmap ./src --format mermaid --output architecture.md
```

### ⚡ 代碼優化 (`optimize`)

```bash
devmind optimize ./src/bottleneck.py --suggest
```

---

## 🚀 快速開始

### 安裝

```bash
pip install devmind-ai
```

### 初始化配置

```bash
devmind init
```

### 基本使用

```bash
# 分析代碼
devmind analyze ./my-project

# 生成文檔
devmind doc ./my-project/src

# 生成思維導圖
devmind mindmap ./my-project/src
```

---

## 📖 配置AI後端

### 使用 Ollama（推薦）

```yaml
ai:
  backend: ollama
  ollama:
    host: http://localhost:11434
    model: codellama
```

### 使用 OpenAI API

```yaml
ai:
  backend: openai
  openai:
    api_key: "sk-your-api-key"
    model: gpt-4
```

---

## 📄 開源協議

[MIT License](./LICENSE)

---

<p align="center">
  Made with ❤️ by DevMind Team
</p>
