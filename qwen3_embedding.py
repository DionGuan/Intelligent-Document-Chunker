# qwen3_embeddings.py
# 自定义 Qwen3 Embeddings 类,调用远程 API 服务
from typing import List
import requests
import logging
from langchain_core.embeddings import Embeddings

logging.basicConfig(level=logging.INFO)

class Qwen3Embeddings(Embeddings):
    """
    Qwen3-Embedding API调用类
    兼容 LangChain Embeddings 接口
    """
    
    def __init__(
        self,
        api_url: str = "your_url",
        api_key: str = "",
        model: str = "Qwen/Qwen3-Embedding",
        timeout: int = 60
    ):
        """
        初始化 Qwen3Embeddings
        
        Args:
            api_url: API 服务地址
            api_key: API密钥
            model: 模型名称
            timeout: 请求超时时间(秒)
        """
        self.api_url = api_url
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        
        logging.info(f"Qwen3 Embeddings 初始化完成,服务地址: {api_url}")
    
    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        调用 Qwen3-Embedding API 获取embeddings
        
        Args:
            texts: 文本列表
            
        Returns:
            embeddings向量列表
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "input": texts
        }
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            
            # 提取 embeddings (按照 OpenAI 格式的返回)
            if "data" in result:
                embeddings = [item["embedding"] for item in result["data"]]
                return embeddings
            else:
                raise ValueError(f"API返回格式错误: {result}")
                
        except requests.exceptions.RequestException as e:
            logging.error(f"API请求失败: {e}")
            raise
        except Exception as e:
            logging.error(f"获取embeddings失败: {e}")
            raise
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        对文档列表进行embedding
        
        Args:
            texts: 文档文本列表
            
        Returns:
            embeddings向量列表
        """
        if not texts:
            return []
        
        logging.info(f"正在对 {len(texts)} 个文档进行embedding...")
        return self._get_embeddings(texts)
    
    def embed_query(self, text: str) -> List[float]:
        """
        对单个查询文本进行embedding
        
        Args:
            text: 查询文本
            
        Returns:
            embedding向量
        """
        result = self._get_embeddings([text])
        return result[0] if result else []
