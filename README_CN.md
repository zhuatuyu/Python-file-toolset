# 视频分辨率重命名工具

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)

一个自动检测视频分辨率并重命名视频文件的 Python 工具。它会根据视频的实际分辨率，在文件名前自动添加对应的分辨率标识（如：1080px_）。

[English](README.md) | 简体中文

## ✨ 特性

- 🎥 自动检测视频分辨率
- 📁 支持批量处理和子目录递归
- 🎬 支持多种视频格式
- 🔄 智能跳过已处理文件
- 📊 处理完成后显示详细统计信息

## 🔧 环境要求

- Python 3.6+
- OpenCV-Python

## 📦 安装方法

1. 克隆仓库：

```bash
git clone https://github.com/zhuatuyu/video-resolution-rename.git
cd video-resolution-rename