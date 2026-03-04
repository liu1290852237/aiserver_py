import argparse
import os
import uuid
from pathlib import Path
from datetime import datetime

import yaml


class Util:
    @staticmethod
    def get_project_dir():
        """1.获取工程根目录路径"""
        root = Path(__file__).resolve().parent.parent.parent
        return f"{root}{os.sep}"  # os.sep是当前系统的分隔符

    @staticmethod
    def get_config_file_path():
        """2.拼接配置文件路径"""
        default_config_file = "config.yaml"
        # 检测与获取配置文件路径
        if os.path.exists(Util.get_project_dir() + "data/." + default_config_file):
            config_file = "data/." + default_config_file
        else:
            config_file = Util.get_project_dir() + default_config_file
        return config_file  # 返回配置文件路径

    @staticmethod
    def get_config():
        """3.加载配置文件"""
        # 创建参数解析器
        parser = argparse.ArgumentParser(description="Server configuration")
        # 添加参数, 指定参数的默认值
        config_file = Util.get_config_file_path()
        parser.add_argument("--config_path", type=str, default=config_file)
        # 解析参数, 返回参数对象
        args = parser.parse_args()
        # 加载配置文件, 返回字典
        print(f"Loading configuration from {args.config_path}")
        with open(args.config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        # 初始化输出目录
        Util.init_output_dirs(config)
        return config
    """ ┌─────────────────────────────────────────┐
        │  1. 创建参数解析器                        │
        │     argparse.ArgumentParser()           │
        └──────────────┬──────────────────────────┘
                       ↓
        ┌─────────────────────────────────────────┐
        │  2. 获取默认配置文件路径                   │
        │     Util.get_config_file_path()         │
        │     → "config.yaml"                     │
        └──────────────┬──────────────────────────┘
                       ↓
        ┌─────────────────────────────────────────┐
        │  3. 注册命令行参数                        │
        │     add_argument("--config_path")       │
        └──────────────┬──────────────────────────┘
                       ↓
        ┌─────────────────────────────────────────┐
        │  4. 解析用户输入的参数                     │
        │     parse_args()                        │
        │     → args.config_path                  │
        └──────────────┬──────────────────────────┘
                       ↓
        ┌─────────────────────────────────────────┐
        │  5. 打开并读取配置文件                     │
        │     with open(...)                      │
        │     yaml.safe_load()                    │
        │     → config 字典                        │
        └──────────────┬──────────────────────────┘
                       ↓
        ┌─────────────────────────────────────────┐
        │  6. 自动创建输出目录                       │
        │     Util.init_output_dirs(config)       │
        └──────────────┬──────────────────────────┘
                       ↓
        ┌─────────────────────────────────────────┐
        │  7. 返回配置字典                          │
        │     return config                       │
        └─────────────────────────────────────────┘
"""
    @staticmethod
    def init_output_dirs(config):
        """4.自动扫描所有层级的output_dir配置并拼接新建文件"""
        results = set()

        # 找到所有的output_dir加入set集合中
        def _traverse(data):
            """递归遍历函数"""
            if isinstance(data, dict):
                if "output_dir" in data:
                    results.add(data["output_dir"])
                for value in data.values():
                    _traverse(value)
            elif isinstance(data, list):
                for item in data:
                    _traverse(item)

        # 将set集合中的元素与根目录拼接成新的路径并创建
        _traverse(config)
        for dir_path in results:
            try:
                os.makedirs(Util.get_project_dir() + dir_path, exist_ok=True)
            except PermissionError:
                print(f"警告，无法创建目录 {dir_path}")

    @staticmethod
    def get_random_file_path(dir: str, ex_name: str):
        """5.获取随机文件保存路径"""
        file_name = f"{datetime.now().date()}_{uuid.uuid4().hex}.{ex_name}"
        file_path = os.path.join(dir, file_name)
        return file_path


if __name__ == "__main__":
    print(Util.get_project_dir())
    print(Util.get_random_file_path(Util.get_project_dir(), "mp3"), "mp3")