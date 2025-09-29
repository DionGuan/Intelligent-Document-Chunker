# document_loader_local.py
import os
import re
import subprocess
from typing import Optional

def load_txt_file(filepath: str) -> str:
    """加载 TXT 文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # 尝试 gbk 编码，常见于中文 Windows 系统创建的 txt
        try:
            with open(filepath, 'r', encoding='gbk') as f:
                return f.read()
        except Exception:
            pass # 如果 gbk 也失败，则抛出原始异常
        raise
    except Exception as e:
        print(f"❌ 读取 TXT 失败: {e}")
        return ""

def load_pdf_and_extract_md(filepath: str) -> str:
    """
    强制使用 MinerU 解析 PDF -> 提取并清理 .md 文件内容
    简化命令：mineru -p <filepath> -o <output_base_dir>
    """
    print("🖼️  正在使用 MinerU 解析 PDF...")

    # --- 确定输出目录 ---
    base_dir = os.path.dirname(filepath)
    pdf_name_without_ext = os.path.splitext(os.path.basename(filepath))[0]
    output_base_dir = os.path.join(base_dir, "output") # 约定输出到 base_dir/output

    try:
        # --- 调用 MinerU (简化命令) ---
        # 确保输出基础目录存在
        os.makedirs(output_base_dir, exist_ok=True)

        # 简化命令，只保留必需参数
        cmd = [
            "mineru",
            "-p", filepath,
            "-o", output_base_dir, # 输出到 base_dir/output
        ]

        print(f"🔧 执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=False, text=False)

        if result.returncode != 0:
            print(f"⚠️  MinerU 执行返回非零码 ({result.returncode})，但将继续尝试读取输出文件。")

        # --- 查找 .md 文件 (现在支持 output/in/auto/in.md 结构) ---
        possible_dirs = [
            os.path.join(output_base_dir, pdf_name_without_ext, "auto"),
            os.path.join(output_base_dir, pdf_name_without_ext),
            output_base_dir
        ]
        
        md_files = []
        for dir_path in possible_dirs:
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                for f in os.listdir(dir_path):
                    if f.endswith('.md') and f.startswith(pdf_name_without_ext):
                        md_files.append(os.path.join(dir_path, f))
        
        if not md_files:
            print(f"❌ 在 {output_base_dir} 中未找到任何 .md 文件。")
            return ""
        
        # 选择第一个找到的 md 文件
        md_path_to_read = md_files[0]
        print(f"📄 找到 Markdown 文件: {md_path_to_read}")

        # --- 读取找到的 .md 文件 ---
        with open(md_path_to_read, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # --- 极简清理 Markdown ---
        cleaned_text = clean_markdown_simple(md_content)
        print("🧹 Markdown 清理完成。")
        return cleaned_text

    except FileNotFoundError:
        print("❌ 未找到 'mineru' 命令。请确保 MinerU 已正确安装，并且 'mineru' 在系统 PATH 中，或者在当前激活的 Python 环境中。")
        return ""
    except Exception as e:
        print(f"❌ MinerU 解析或文件处理异常: {e}")
        import traceback
        traceback.print_exc() # 打印详细堆栈信息，便于调试
        return ""

def clean_markdown_simple(md_text: str) -> str:
    """
    极简清理 Markdown：
    - 移除表格行（以 | 开头或包含 |---|）
    - 移除代码块（```）
    - 合并多余空行
    """
    if not md_text:
        return md_text

    lines = md_text.split('\n')
    cleaned_lines = []
    in_code_block = False

    for line in lines:
        # 跳过代码块
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # 跳过表格行 (更宽松的匹配)
        if (line.strip().startswith('|') and line.strip().endswith('|')) or \
           re.search(r'\|[-\s:]+\|', line): # 匹配 |----| 或 |:---| 等表头分隔符
            continue

        # 跳过多余空行 (保留一个空行)
        if line.strip() == '':
            if cleaned_lines and cleaned_lines[-1].strip() == '':
                 continue # 如果上一行也是空行，则跳过
            # else: 添加空行

        # 保留标题和普通文本
        cleaned_lines.append(line)

    # 去除首尾空白
    return '\n'.join(cleaned_lines).strip()