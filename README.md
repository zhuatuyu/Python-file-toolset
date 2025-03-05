# Video Resolution Rename Tool

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)

A Python tool that automatically detects video resolution and renames video files by adding resolution prefix (e.g., 1080px_) based on their actual resolution.

English | [简体中文](README_CN.md)

## ✨ Features

- 🎥 Automatic video resolution detection
- 📁 Batch processing with subdirectory support
- 🎬 Multiple video format support
- 🔄 Smart skipping of already processed files
- 📊 Detailed statistics after processing

## 🔧 Requirements

- Python 3.6+
- OpenCV-Python

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/zhuatuyu/video-resolution-rename.git
cd video-resolution-rename
```

## 功能模块

1. `video_rename.py`: 视频文件批量重命名工具，自动添加分辨率信息
2. `video_subtitle.py`: 视频字幕生成工具，支持多语言识别和翻译
3. `video_screenshot.py`: 视频截图工具