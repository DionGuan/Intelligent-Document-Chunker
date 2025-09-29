# main.py
import os
import sys
from typing import Optional, List

# 确保导入路径正确
# 假设 semantic_chunker_local.py 和 document_loader_local.py 在同一目录
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from semantic_chunker_local import LocalSemanticChunker
# 导入新的 PDF 处理函数
from document_loader_local import load_txt_file, load_pdf_and_extract_md

def get_file_path() -> Optional[str]:
    """获取文件路径"""
    print("\n📂 请选择要切分的文档（支持 .txt 或 .pdf）")
    print("👉 方法1：直接把文件拖入终端窗口")
    print("👉 方法2：手动输入完整路径")
    print("-" * 60)
    try:
        # 去除用户可能误加的引号
        path = input("请输入文件路径: ").strip().strip('"').strip("'")
        # 规范化路径分隔符
        path = os.path.normpath(path)
        if os.path.exists(path) and os.path.isfile(path):
            return path
        else:
            print(f"❌ 文件不存在或不是有效文件: {path}")
            return None
    except KeyboardInterrupt:
        print("\n👋 用户取消")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 输入错误: {e}")
        return None

def save_chunks_to_output_folder(chunks: List[str], original_file_path: str):
    """
    将 chunks 保存到与原始文件同级的 output 文件夹内。
    文件名格式: 原始文件名_without_ext.chunk.1.txt, .chunk.2.txt, ...
    同时创建一个合并的txt文件，包含所有chunk
    """
    if not chunks:
        print("⚠️  没有 chunks 需要保存。")
        return

    base_dir = os.path.dirname(original_file_path)
    original_name_without_ext = os.path.splitext(os.path.basename(original_file_path))[0]
    output_dir = os.path.join(base_dir, "output", original_name_without_ext) # 保存在 output/子文件夹名/ 下

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 保存每个chunk到单独文件
    saved_files = []
    for i, chunk in enumerate(chunks, start=1):
        filename = f"{original_name_without_ext}.chunk.{i}.txt"
        file_path = os.path.join(output_dir, filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(chunk)
            saved_files.append(file_path)
            print(f"💾 已保存 Chunk {i} 到: {file_path}")
        except Exception as e:
            print(f"❌ 保存 Chunk {i} 失败: {e}")

    # 创建合并的txt文件
    combined_filename = f"{original_name_without_ext}.all_chunks.txt"
    combined_file_path = os.path.join(output_dir, combined_filename)
    
    try:
        with open(combined_file_path, 'w', encoding='utf-8') as f:
            for i, chunk in enumerate(chunks, start=1):
                f.write(f"=== Chunk {i} ===\n{chunk}\n\n")
        print(f"✅ 已创建合并文件: {combined_file_path}")
    except Exception as e:
        print(f"❌ 创建合并文件失败: {e}")

    print(f"✅ 总共保存了 {len(saved_files)} 个 chunks 到 {output_dir}")
def main():
    file_path = get_file_path()
    if not file_path:
        return

    print(f"\n📂 正在加载文件: {file_path}")
    ext = os.path.splitext(file_path)[1].lower()

    text = ""
    if ext == ".txt":
        text = load_txt_file(file_path)
        if not text:
             print("❌ 未能从 TXT 文件中读取有效文本。")
             return
    elif ext == ".pdf":
        # --- 强制调用简化后的 MinerU 并读取 Markdown ---
        text = load_pdf_and_extract_md(file_path)
        if not text:
             print("❌ 未能通过 MinerU 从 PDF 中提取有效文本。")
             return
        print(f"📖 提取并清理后的文本长度: {len(text)} 字符")
    else:
        print("❌ 不支持的文件格式，请提供 .txt 或 .pdf 文件。")
        return

    if len(text) == 0:
         print("⚠️  提取的文本为空，将不进行切分。")
         return


    # --- 语义切分 ---
    print("\n✂️  正在初始化语义切分器...")
    # @todo 未来可在此处根据文件类型或用户输入调整参数
    try:
        chunker = LocalSemanticChunker(
            embedding_model_name="sentence-transformers/all-MiniLM-L6-v2", # @todo 换 qwen3-embedding
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=95, # @todo 可动态调整
            device="cpu" # @todo 可根据环境调整为 "cuda"
        )
    except Exception as e:
         print(f"❌ 初始化语义切分器失败: {e}")
         import traceback
         traceback.print_exc()
         return

    print("🧠 正在进行语义切分...")
    try:
        chunks = chunker.split_text(text)
        print(f"🎯 语义切分完成，总共切分出 {len(chunks)} 个块。")
    except Exception as e:
         print(f"❌ 语义切分过程中发生错误: {e}")
         import traceback
         traceback.print_exc() # 打印详细堆栈信息，便于调试
         return # 切分失败则不继续

    if not chunks:
         print("⚠️  语义切分结果为空。")
         return

    # --- 保存结果 ---
    print("\n💾 正在保存切分结果...")
    save_chunks_to_output_folder(chunks, file_path)

    # --- (可选) 在终端打印预览 ---
    print("\n👀 切分结果预览 (前 3 个块):")
    for i in range(min(3, len(chunks))):
        print(f"\n--- Chunk {i+1} ({len(chunks[i])} 字符) ---")
        preview_text = chunks[i][:300] + "..." if len(chunks[i]) > 300 else chunks[i]
        print(preview_text)


if __name__ == "__main__":
    main()