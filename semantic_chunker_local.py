# semantic_chunker_local.py
# 标准的 LocalSemanticChunker 类定义
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List, Optional
import logging

logging.basicConfig(level=logging.INFO)

class LocalSemanticChunker:
    def __init__(
        self,
        embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2", # @todo 换 qwen3-embedding
        # embedding_model_name: str = "qwen3-embedding",@Todo
        # embedding_model_kwargs: Optional[dict] = None,
        breakpoint_threshold_type: str = "percentile",
        breakpoint_threshold_amount: Optional[float] = 95,
        device: str = "cpu"
    ):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            model_kwargs={"device": device},
            encode_kwargs={"normalize_embeddings": True}
        )

        self.text_splitter = SemanticChunker(
            embeddings=self.embedding_model,
            breakpoint_threshold_type=breakpoint_threshold_type,
            breakpoint_threshold_amount=breakpoint_threshold_amount
        )

        logging.info(f"✅ 本地语义切分器加载完成，使用模型: {embedding_model_name}")

    def split_text(self, text: str) -> List[str]:
        if not text.strip():
            return []
        try:
            chunks = self.text_splitter.split_text(text)
            logging.info(f"📄 文本切分为 {len(chunks)} 个语义块")
            return chunks
        except Exception as e:
            logging.error(f"❌ 文本切分失败: {e}")
            raise # 重新抛出异常，让调用者处理
