"""
文件工具类
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import List, Optional, Union
import logging


class FileUtils:
    """文件工具类"""
    
    @staticmethod
    def ensure_dir(path: Union[str, Path]) -> Path:
        """
        确保目录存在
        
        Args:
            path: 目录路径
            
        Returns:
            Path: 目录路径对象
        """
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def get_file_hash(file_path: Union[str, Path], algorithm: str = "md5") -> str:
        """
        获取文件哈希值
        
        Args:
            file_path: 文件路径
            algorithm: 哈希算法
            
        Returns:
            str: 文件哈希值
        """
        hash_obj = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    
    @staticmethod
    def get_file_size(file_path: Union[str, Path]) -> int:
        """
        获取文件大小
        
        Args:
            file_path: 文件路径
            
        Returns:
            int: 文件大小（字节）
        """
        return os.path.getsize(file_path)
    
    @staticmethod
    def list_files(directory: Union[str, Path], 
                   pattern: str = "*", 
                   recursive: bool = False) -> List[Path]:
        """
        列出目录中的文件
        
        Args:
            directory: 目录路径
            pattern: 文件模式
            recursive: 是否递归
            
        Returns:
            List[Path]: 文件路径列表
        """
        directory = Path(directory)
        if recursive:
            return list(directory.rglob(pattern))
        else:
            return list(directory.glob(pattern))
    
    @staticmethod
    def copy_file(src: Union[str, Path], 
                  dst: Union[str, Path], 
                  overwrite: bool = False) -> bool:
        """
        复制文件
        
        Args:
            src: 源文件路径
            dst: 目标文件路径
            overwrite: 是否覆盖
            
        Returns:
            bool: 是否成功
        """
        try:
            src = Path(src)
            dst = Path(dst)
            
            if not src.exists():
                logging.error(f"源文件不存在: {src}")
                return False
            
            if dst.exists() and not overwrite:
                logging.error(f"目标文件已存在: {dst}")
                return False
            
            # 确保目标目录存在
            dst.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(src, dst)
            return True
            
        except Exception as e:
            logging.error(f"复制文件失败: {e}")
            return False
    
    @staticmethod
    def move_file(src: Union[str, Path], 
                  dst: Union[str, Path], 
                  overwrite: bool = False) -> bool:
        """
        移动文件
        
        Args:
            src: 源文件路径
            dst: 目标文件路径
            overwrite: 是否覆盖
            
        Returns:
            bool: 是否成功
        """
        try:
            src = Path(src)
            dst = Path(dst)
            
            if not src.exists():
                logging.error(f"源文件不存在: {src}")
                return False
            
            if dst.exists() and not overwrite:
                logging.error(f"目标文件已存在: {dst}")
                return False
            
            # 确保目标目录存在
            dst.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.move(str(src), str(dst))
            return True
            
        except Exception as e:
            logging.error(f"移动文件失败: {e}")
            return False
    
    @staticmethod
    def delete_file(file_path: Union[str, Path]) -> bool:
        """
        删除文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否成功
        """
        try:
            file_path = Path(file_path)
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            logging.error(f"删除文件失败: {e}")
            return False
    
    @staticmethod
    def clean_directory(directory: Union[str, Path], 
                       pattern: str = "*",
                       keep_dirs: bool = True) -> int:
        """
        清理目录
        
        Args:
            directory: 目录路径
            pattern: 文件模式
            keep_dirs: 是否保留目录
            
        Returns:
            int: 删除的文件数量
        """
        directory = Path(directory)
        if not directory.exists():
            return 0
        
        deleted_count = 0
        for item in directory.glob(pattern):
            if item.is_file():
                item.unlink()
                deleted_count += 1
            elif item.is_dir() and not keep_dirs:
                shutil.rmtree(item)
                deleted_count += 1
        
        return deleted_count
