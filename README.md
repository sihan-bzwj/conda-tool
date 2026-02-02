# Conda 一站式清理与管理工具 / Conda All-in-One Cleanup & Management Tool

[中文](#中文) | [English](#english)

---

## 中文

### 简介

一个简洁的命令行工具，用于安全清理Anaconda缓存和管理虚拟环境。支持中英文双语界面。

### 功能特点

- 🧹 **一键安全清理缓存**：清理Conda和Pip的缓存文件，不删除任何环境
- 📁 **查看与管理环境**：列出所有Conda环境，并可安全删除（保护base环境）
- 📊 **查看磁盘占用**：快速分析Anaconda目录的空间使用情况
- 🌐 **双语支持**：支持中文和英文界面，可随时切换

### 安装与使用

1. **前提条件**

   - 已安装Anaconda或Miniconda
   - Python 3.6 或更高版本
2. **下载与运行**

   ```bash
   # 克隆仓库或下载脚本
   git clone https://github.com/yourusername/conda-tool.git
   cd conda-tool

   # 运行工具
   python conda_tool.py

   ```

3. **首次运行**

   - 程序会自动检测系统语言
   - 可在主菜单中选择选项4切换语言
   - 语言选择会保存，下次启动自动应用

### 使用说明

1. **一键清理缓存**（选项1）

   - 安全清理所有缓存文件
   - 不会删除任何虚拟环境
2. **环境管理**（选项2）

   - 查看所有Conda环境
   - 选择序号删除不需要的环境
   - 自动保护base环境和当前使用环境
3. **磁盘分析**（选项3）

   - 查看envs和pkgs目录大小
   - 识别占用空间的主要目录

### 注意事项

- 删除环境前请确认，操作不可逆
- 建议在Anaconda Prompt中运行此脚本
- base环境受保护，无法删除
- 无法删除当前正在使用的环境

### 贡献

欢迎提交Issue和Pull Request！

---

## English

### Introduction

A concise command-line tool for safely cleaning Anaconda cache and managing virtual environments. Supports bilingual interface (Chinese/English).

### Features

- 🧹 **Safe One-click Cache Cleanup**: Clean Conda and Pip cache files without deleting any environments
- 📁 **View & Manage Environments**: List all Conda environments and safely delete them (base environment protected)
- 📊 **Check Disk Usage**: Quickly analyze space usage of Anaconda directories
- 🌐 **Bilingual Support**: Chinese and English interface, switchable at any time

### Installation & Usage

1. **Prerequisites**

   - Anaconda or Miniconda installed
   - Python 3.6 or higher
2. **Download & Run**
   bash

   ```
   # Clone repository or download script
   git clone https://github.com/yourusername/conda-tool.git
   cd conda-tool

   # Run the tool
   python conda_tool_bilingual.py
   ```
3. **First Run**

   - Program auto-detects system language
   - Switch language via option 4 in main menu
   - Language preference is saved for future sessions

### Usage Guide

1. **One-click Cache Cleanup** (Option 1)

   - Safely clean all cache files
   - No virtual environments will be deleted
2. **Environment Management** (Option 2)

   - View all Conda environments
   - Delete unnecessary environments by number
   - Automatic protection for base and current environment
3. **Disk Analysis** (Option 3)

   - Check size of envs and pkgs directories
   - Identify space-consuming directories

### Important Notes

- Confirm before deleting environments, operation is irreversible
- Recommended to run in Anaconda Prompt
- Base environment is protected from deletion
- Cannot delete currently active environment

### Contributing

Issues and Pull Requests are welcome!