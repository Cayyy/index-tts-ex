"""
文本工具类
"""

import re
import unicodedata
from typing import List, Optional, Dict, Any
import logging


class TextUtils:
    """文本工具类"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        清理文本
        
        Args:
            text: 输入文本
            
        Returns:
            str: 清理后的文本
        """
        if not text:
            return ""
        
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text.strip())
        
        # 移除控制字符
        text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C' or char in '\n\t')
        
        return text
    
    @staticmethod
    def split_text(text: str, max_length: int = 500) -> List[str]:
        """
        分割长文本
        
        Args:
            text: 输入文本
            max_length: 最大长度
            
        Returns:
            List[str]: 分割后的文本列表
        """
        if len(text) <= max_length:
            return [text]
        
        # 按句子分割
        sentences = re.split(r'[。！？.!?]', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if not sentence.strip():
                continue
            
            # 添加标点符号
            if sentence != sentences[-1]:
                sentence += "。"
            
            if len(current_chunk + sentence) <= max_length:
                current_chunk += sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    @staticmethod
    def extract_emotions(text: str) -> Dict[str, float]:
        """
        从文本中提取情感信息
        
        Args:
            text: 输入文本
            
        Returns:
            Dict[str, float]: 情感字典
        """
        # 简单的情感关键词匹配
        emotion_keywords = {
            "happy": ["高兴", "开心", "快乐", "愉快", "兴奋", "喜悦", "哈哈", "呵呵"],
            "sad": ["悲伤", "难过", "伤心", "痛苦", "沮丧", "失望", "哭泣", "眼泪"],
            "angry": ["愤怒", "生气", "恼火", "愤怒", "气愤", "暴怒", "讨厌", "恨"],
            "afraid": ["害怕", "恐惧", "担心", "紧张", "焦虑", "恐慌", "惊吓"],
            "surprised": ["惊讶", "吃惊", "意外", "震惊", "惊奇", "没想到", "哇"],
            "calm": ["平静", "安静", "冷静", "镇定", "宁静", "温和", "温柔"]
        }
        
        emotions = {emotion: 0.0 for emotion in emotion_keywords.keys()}
        text_lower = text.lower()
        
        for emotion, keywords in emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                emotions[emotion] = min(count / len(keywords), 1.0)
        
        return emotions
    
    @staticmethod
    def validate_text(text: str, 
                     min_length: int = 1, 
                     max_length: int = 1000,
                     allowed_chars: Optional[str] = None) -> bool:
        """
        验证文本
        
        Args:
            text: 输入文本
            min_length: 最小长度
            max_length: 最大长度
            allowed_chars: 允许的字符集
            
        Returns:
            bool: 是否有效
        """
        if not text:
            return False
        
        if len(text) < min_length or len(text) > max_length:
            return False
        
        if allowed_chars:
            for char in text:
                if char not in allowed_chars:
                    return False
        
        return True
    
    @staticmethod
    def format_text_for_tts(text: str) -> str:
        """
        为 TTS 格式化文本
        
        Args:
            text: 输入文本
            
        Returns:
            str: 格式化后的文本
        """
        # 清理文本
        text = TextUtils.clean_text(text)
        
        # 处理数字
        text = re.sub(r'(\d+)', r'\1', text)
        
        # 处理标点符号
        text = re.sub(r'([。！？])([^。！？])', r'\1 \2', text)
        
        # 处理英文和中文混合
        text = re.sub(r'([a-zA-Z])([\u4e00-\u9fff])', r'\1 \2', text)
        text = re.sub(r'([\u4e00-\u9fff])([a-zA-Z])', r'\1 \2', text)
        
        return text
    
    @staticmethod
    def count_words(text: str) -> int:
        """
        统计词数
        
        Args:
            text: 输入文本
            
        Returns:
            int: 词数
        """
        # 简单的中英文词数统计
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
        return chinese_chars + english_words
    
    @staticmethod
    def estimate_duration(text: str, words_per_minute: int = 200) -> float:
        """
        估算语音时长
        
        Args:
            text: 输入文本
            words_per_minute: 每分钟词数
            
        Returns:
            float: 估算时长（秒）
        """
        word_count = TextUtils.count_words(text)
        duration_minutes = word_count / words_per_minute
        return duration_minutes * 60
