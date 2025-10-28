#!/usr/bin/env python3
"""
XML 特殊字符清理工具

用于处理 OWL 文件中的 XML 预定义字符，确保解析功能正常运行。
主要处理 <rdfs:label xml:lang="zh"> 和 <obo:IAO_0000115 xml:lang="zh"> 标签中的特殊字符。
"""

import re
import os
from typing import Dict, List, Tuple


class XMLCleaner:
    """XML 特殊字符清理器"""
    
    # XML 预定义字符映射表
    XML_ESCAPE_MAP = {
        '&': '&amp;',    # 必须首先处理，避免重复转义
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&apos;'
    }
    
    # 反向映射表（用于恢复）
    XML_UNESCAPE_MAP = {
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&apos;': "'"
    }
    
    def __init__(self):
        """初始化 XML 清理器"""
        self.cleaned_count = 0
        self.error_count = 0
    
    def escape_xml_chars(self, text: str) -> str:
        """
        转义 XML 特殊字符
        
        Args:
            text: 需要转义的文本
            
        Returns:
            str: 转义后的文本
        """
        if not text:
            return text
            
        # 按顺序转义，& 必须首先处理
        escaped_text = text
        for char, replacement in self.XML_ESCAPE_MAP.items():
            escaped_text = escaped_text.replace(char, replacement)
        
        return escaped_text
    
    def unescape_xml_chars(self, text: str) -> str:
        """
        恢复 XML 特殊字符
        
        Args:
            text: 需要恢复的文本
            
        Returns:
            str: 恢复后的文本
        """
        if not text:
            return text
            
        # 按顺序恢复，&amp; 必须最后处理
        unescaped_text = text
        for replacement, char in self.XML_UNESCAPE_MAP.items():
            unescaped_text = unescaped_text.replace(replacement, char)
        
        return unescaped_text
    
    def clean_owl_file(self, input_file: str, output_file: str = None) -> str:
        """
        清理 OWL 文件中的 XML 特殊字符
        
        Args:
            input_file: 输入 OWL 文件路径
            output_file: 输出文件路径，如果为 None 则自动生成
            
        Returns:
            str: 输出文件路径
        """
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"输入文件不存在: {input_file}")
        
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_cleaned.owl"
        
        print(f"🧹 开始清理 OWL 文件: {input_file}")
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 清理内容
            cleaned_content = self._clean_xml_content(content)
            
            # 写入清理后的文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            print(f"✅ 清理完成，输出文件: {output_file}")
            print(f"📊 统计信息:")
            print(f"   - 清理的标签数量: {self.cleaned_count}")
            print(f"   - 错误数量: {self.error_count}")
            
            return output_file
            
        except Exception as e:
            print(f"❌ 清理过程中发生错误: {str(e)}")
            self.error_count += 1
            raise
    
    def _clean_xml_content(self, content: str) -> str:
        """
        清理 XML 内容中的特殊字符
        
        Args:
            content: XML 内容
            
        Returns:
            str: 清理后的内容
        """
        # 定义需要清理的标签模式
        patterns = [
            # <rdfs:label xml:lang="zh">...</rdfs:label>
            (r'<rdfs:label xml:lang="zh">(.*?)</rdfs:label>', 'rdfs:label'),
            # <obo:IAO_0000115 xml:lang="zh">...</obo:IAO_0000115>
            (r'<obo:IAO_0000115 xml:lang="zh">(.*?)</obo:IAO_0000115>', 'obo:IAO_0000115'),
            # 也处理没有 xml:lang 属性的情况
            (r'<rdfs:label>(.*?)</rdfs:label>', 'rdfs:label'),
            (r'<obo:IAO_0000115>(.*?)</obo:IAO_0000115>', 'obo:IAO_0000115')
        ]
        
        cleaned_content = content
        
        for pattern, tag_name in patterns:
            def replace_func(match):
                original_text = match.group(1)
                escaped_text = self.escape_xml_chars(original_text)
                
                if escaped_text != original_text:
                    self.cleaned_count += 1
                    print(f"  🔧 清理 {tag_name}: '{original_text}' -> '{escaped_text}'")
                
                return match.group(0).replace(original_text, escaped_text)
            
            try:
                cleaned_content = re.sub(pattern, replace_func, cleaned_content, flags=re.DOTALL)
            except Exception as e:
                print(f"  ⚠️  处理 {tag_name} 时发生错误: {str(e)}")
                self.error_count += 1
        
        return cleaned_content
    
    def validate_xml_escaping(self, text: str) -> bool:
        """
        验证文本是否正确转义了 XML 特殊字符
        
        Args:
            text: 需要验证的文本
            
        Returns:
            bool: 是否正确转义
        """
        if not text:
            return True
        
        # 检查是否包含未转义的 XML 特殊字符
        unescaped_chars = ['<', '>', '&', '"', "'"]
        for char in unescaped_chars:
            if char in text:
                return False
        
        return True
    
    def get_cleaning_stats(self) -> Dict[str, int]:
        """
        获取清理统计信息
        
        Returns:
            Dict[str, int]: 统计信息
        """
        return {
            'cleaned_count': self.cleaned_count,
            'error_count': self.error_count
        }
    
    def reset_stats(self):
        """重置统计信息"""
        self.cleaned_count = 0
        self.error_count = 0


def clean_owl_file(input_file: str, output_file: str = None) -> str:
    """
    便捷函数：清理 OWL 文件
    
    Args:
        input_file: 输入 OWL 文件路径
        output_file: 输出文件路径
        
    Returns:
        str: 输出文件路径
    """
    cleaner = XMLCleaner()
    return cleaner.clean_owl_file(input_file, output_file)


def escape_xml_text(text: str) -> str:
    """
    便捷函数：转义 XML 文本
    
    Args:
        text: 需要转义的文本
        
    Returns:
        str: 转义后的文本
    """
    cleaner = XMLCleaner()
    return cleaner.escape_xml_chars(text)


def unescape_xml_text(text: str) -> str:
    """
    便捷函数：恢复 XML 文本
    
    Args:
        text: 需要恢复的文本
        
    Returns:
        str: 恢复后的文本
    """
    cleaner = XMLCleaner()
    return cleaner.unescape_xml_chars(text)


# === 测试和示例 ===
if __name__ == "__main__":
    # 测试 XML 字符转义
    print("🧪 测试 XML 字符转义...")
    
    test_cases = [
        "这是一个包含 < 和 > 的文本",
        "文本中有 & 符号",
        '文本中有 " 双引号',
        "文本中有 ' 单引号",
        "混合字符: <tag>content</tag> & \"quoted\"",
        "正常文本，无需转义",
        ""
    ]
    
    cleaner = XMLCleaner()
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\n测试 {i}: '{test_text}'")
        escaped = cleaner.escape_xml_chars(test_text)
        unescaped = cleaner.unescape_xml_chars(escaped)
        is_valid = cleaner.validate_xml_escaping(escaped)
        
        print(f"  转义后: '{escaped}'")
        print(f"  恢复后: '{unescaped}'")
        print(f"  是否有效: {is_valid}")
        print(f"  往返一致: {test_text == unescaped}")
    
    # 测试 OWL 文件清理（如果文件存在）
    owl_file = "./psi-ms-zh.owl"
    if os.path.exists(owl_file):
        print(f"\n🧹 测试 OWL 文件清理: {owl_file}")
        try:
            output_file = clean_owl_file(owl_file)
            print(f"✅ 清理完成: {output_file}")
        except Exception as e:
            print(f"❌ 清理失败: {str(e)}")
    else:
        print(f"\n⚠️  OWL 文件不存在: {owl_file}")
