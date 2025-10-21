"""
Services untuk inisialisasi LLM, embeddings, dan vector store
"""
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

from config import Config


class LLMService:
    """Service untuk mengelola Language Model"""
    
    @staticmethod
    def initialize(api_key: str):
        """Inisialisasi ChatOpenAI LLM"""
        return ChatOpenAI(
            model=Config.LLM_MODEL,
            api_key=api_key,
            temperature=Config.LLM_TEMPERATURE
        )


class EmbeddingService:
    """Service untuk mengelola embeddings (gratis dan lokal)"""
    
    @staticmethod
    @st.cache_resource
    def initialize():
        """Inisialisasi HuggingFace embeddings dengan caching"""
        return HuggingFaceEmbeddings(
            model_name=Config.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )


class VectorStoreService:
    """Service untuk mengelola Qdrant Vector Store"""
    
    @staticmethod
    @st.cache_resource
    def initialize(_embeddings, qdrant_url: str, qdrant_api_key: str):
        """
        Inisialisasi Qdrant Vector Store dari existing collection
        
        Args:
            _embeddings: HuggingFace embeddings instance
            qdrant_url: URL Qdrant Cloud
            qdrant_api_key: API key Qdrant
            
        Returns:
            QdrantVectorStore instance
        """
        try:
            qdrant = QdrantVectorStore.from_existing_collection(
                embedding=_embeddings,
                collection_name=Config.COLLECTION_NAME,
                url=qdrant_url,
                api_key=qdrant_api_key,
                prefer_grpc=False
            )
            return qdrant
        except Exception as e:
            st.error(f"❌ Gagal terhubung ke Qdrant: {str(e)}")
            st.info("Pastikan Anda sudah menjalankan: python setup_vectordb.py")
            st.stop()


def initialize_services(api_keys: dict):
    """
    Inisialisasi semua services yang diperlukan
    
    Args:
        api_keys: Dictionary berisi semua API keys
        
    Returns:
        Tuple of (llm, embeddings, vector_store)
    """
    llm = LLMService.initialize(api_keys["openai_api_key"])
    embeddings = EmbeddingService.initialize()
    vector_store = VectorStoreService.initialize(
        embeddings,
        api_keys["qdrant_url"],
        api_keys["qdrant_api_key"]
    )
    
    return llm, embeddings, vector_store