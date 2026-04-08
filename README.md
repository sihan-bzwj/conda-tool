# 🛠️ Conda All-in-One Cleanup & Management Tool

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> A concise and powerful command-line utility for safely cleaning Anaconda cache and managing virtual environments.
>
> 一个简洁高效的命令行工具，专为安全清理 Anaconda 缓存与管理虚拟环境而设计。

🌍 **Languages:** [中文文档](#-中文文档) | [English Documentation](#-english-documentation)

---

## 🇨🇳 中文文档

### 💡 简介

本工具旨在解决 Conda 环境臃肿与多环境管理痛点。通过全交互式终端菜单，提供缓存清理、环境增删及磁盘扫描功能，内置安全保护机制，确保您的工作环境数据安全。

### ✨ 核心功能

* 🧹 **一键安全清理**：深度清除 Conda 与 Pip 的冗余缓存文件，**绝对不触碰**任何已有虚拟环境。
* 📁 **可视化环境总管**：清晰列出所有 Conda 环境并支持按序号一键删除。内置**防误删保护机制**（严禁删除 `base` 根环境及当前激活的环境）。
* 📊 **磁盘空间体检**：秒级扫描并分析 `envs` 和 `pkgs` 核心目录，精准定位磁盘空间占用大户。
* 🌐 **无缝双语切换**：原生支持中英双语，一键切换并自动持久化记忆用户偏好。

### 🚀 安装与使用

#### 前提条件

* 已正确安装 Anaconda 或 Miniconda
* Python 3.6 或更高版本

#### 快速启动

建议在 **Anaconda Prompt** 或已配置 Conda 环境变量的终端中执行以下命令：

# 1. 克隆仓库或下载源码

git clone <https://github.com/sihan-bzwj/conda-tool.git>
cd conda-tool

# 2. 运行工具

python conda_tool.py

*注：首次运行时，程序会自动检测系统语言。您也可通过主菜单的“选项 4”手动切换，配置将在下次启动时自动生效。*

### ⚠️ 注意事项

1. **操作不可逆**：删除虚拟环境前请务必仔细核对环境名称。
2. **环境锁定**：受保护的 `base` 环境及当前正在使用的环境无法通过此工具删除。若需删除当前环境，请先 `conda activate` 切换至其他环境。

### 🤝 参与贡献

欢迎提交 Issue 报告 Bug，或发起 Pull Request 提供功能改进！

---

## 🇬🇧 English Documentation

### 💡 Introduction

A lightweight, interactive command-line utility designed to solve Anaconda cache bloat and simplify virtual environment management. It offers a secure way to free up disk space and manage environments through an intuitive menu system.

### ✨ Features

* 🧹 **Safe Cache Cleanup:** One-click purge of Conda and Pip cache files with **zero risk** to your existing virtual environments.
* 📁 **Environment Manager:** Visually list and selectively remove unused Conda environments. Includes **built-in safeguards** (the `base` environment and the currently active environment are strictly protected from deletion).
* 📊 **Disk Analysis:** Rapidly scan the `envs` and `pkgs` directories to identify the primary sources of disk space consumption.
* 🌐 **Bilingual UI:** Native English and Chinese support with persistent preference saving across sessions.

### 🚀 Installation & Usage

#### Prerequisites

* Anaconda or Miniconda installed
* Python 3.6 or higher

#### Quick Start

It is highly recommended to run this script within the **Anaconda Prompt** or a terminal where Conda is initialized:

# 1. Clone the repository or download the script

git clone <https://github.com/sihan-bzwj/conda-tool.git>
cd conda-tool

# 2. Run the tool

python conda_tool.py

*Note: On the first run, the program auto-detects your system language. You can manually switch languages via Option 4 in the main menu, and your preference will be saved for future sessions.*

### ⚠️ Important Notes

1. **Irreversible Actions:** Please confirm the environment name carefully before proceeding with deletion.
2. **Environment Locks:** The `base` environment and your currently active environment are locked. To delete an active environment, you must `conda activate` a different one first.

### 🤝 Contributing

Issues and Pull Requests are warmly welcomed to help improve this tool!
