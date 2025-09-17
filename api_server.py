#!/usr/bin/env python3
"""
IndexTTS 二次开发项目 API 服务器启动脚本
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.api.api_server import main

if __name__ == "__main__":
    main()
