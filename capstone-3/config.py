"""
Konfigurasi aplikasi dan environment variables
"""
import os
import streamlit as st


class Config:
    """Class untuk mengelola konfigurasi aplikasi"""
    
    # Model configuration
    LLM_MODEL = "gpt-4o-mini"
    LLM_TEMPERATURE = 0.7
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Qdrant configuration
    COLLECTION_NAME = "imdb_movies"
    
    # Search configuration
    DEFAULT_SEARCH_K = 10
    
    # Pricing (per 1M tokens)
    INPUT_TOKEN_PRICE_USD = 0.15
    OUTPUT_TOKEN_PRICE_USD = 0.6
    USD_TO_IDR = 17_000
    
    @staticmethod
    def load_api_keys():
        """Muat API keys dari Streamlit secrets atau .env file"""
        try:
            # Coba muat dari Streamlit secrets
            openai_key = st.secrets["OPENAI_API_KEY"]
            qdrant_url = st.secrets["QDRANT_URL"]
            qdrant_key = st.secrets["QDRANT_API_KEY"]
        except (FileNotFoundError, KeyError):
            # Fallback ke .env file
            from dotenv import load_dotenv
            load_dotenv()
            openai_key = os.getenv("OPENAI_API_KEY")
            qdrant_url = os.getenv("QDRANT_URL")
            qdrant_key = os.getenv("QDRANT_API_KEY")
        
        return {
            "openai_api_key": openai_key,
            "qdrant_url": qdrant_url,
            "qdrant_api_key": qdrant_key
        }
    
    @staticmethod
    def validate_api_keys(keys: dict) -> bool:
        """Validasi keberadaan semua API keys"""
        return all(keys.values())