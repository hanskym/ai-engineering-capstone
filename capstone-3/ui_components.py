"""
Streamlit UI components
"""
import random
import streamlit as st
from utils import format_currency, format_large_number


class UIComponents:
    """Class untuk mengelola UI components"""
    
    @staticmethod
    def setup_page_config():
        """Setup konfigurasi halaman Streamlit"""
        st.set_page_config(
            page_title="IMDB Movie Assistant",
            page_icon="🎬",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    @staticmethod
    def render_header():
        """Render header aplikasi"""
        st.title("🎬 IMDB Movie Recommendation Agent")
        st.markdown("*AI-powered movie recommendations using RAG Agent*")
        st.markdown("---")
    
    @staticmethod
    def render_sidebar():
        """Render sidebar dengan informasi aplikasi"""
        with st.sidebar:
            st.header("📖 Tentang Aplikasi")
            
            st.info("""
            **Tech Stack:**
            - 🤖 LLM: GPT-4o Mini
            - 🔢 Embeddings: HuggingFace (GRATIS)
            - 💾 Vector DB: Qdrant Cloud
            - 🛠️ Framework: LangChain + LangGraph
            - 🎬 Dataset: IMDB Top 1000 Movies
            """)
            
            st.success("✅ Terhubung ke Qdrant Cloud")
            
            # Clear history button
            if st.button("🗑️ Hapus Riwayat Chat", use_container_width=True):
                from utils import SessionStateManager
                SessionStateManager.clear_history()
                st.rerun()
            
            st.markdown("---")
            st.caption("Dibuat dengan ❤️ menggunakan Streamlit")
    
    @staticmethod
    def render_chat_history():
        """Render chat history dari session state"""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    @staticmethod
    def render_response_metrics(response: dict):
        """
        Render metrics untuk response
        
        Args:
            response: Dictionary berisi response data
        """
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("📊 Token Usage"):
                st.metric(
                    "Input Tokens",
                    format_large_number(response["total_input_tokens"])
                )
                st.metric(
                    "Output Tokens",
                    format_large_number(response["total_output_tokens"])
                )
                st.metric(
                    "Total Tokens",
                    format_large_number(
                        response["total_input_tokens"] + 
                        response["total_output_tokens"]
                    )
                )
        
        with col2:
            with st.expander("💰 Cost"):
                st.metric(
                    "Cost (IDR)",
                    format_currency(response["idr_price"], "IDR")
                )
                st.metric(
                    "Cost (USD)",
                    format_currency(response["usd_price"], "USD")
                )
                st.caption(f"⏰ {response['timestamp']}")
    
    @staticmethod
    def render_footer():
        """Render footer aplikasi"""
        st.markdown("---")
        st.caption(
            "🎬 IMDB Movie RAG Agent | "
            "Powered by LangChain, LangGraph & Qdrant"
        )
    
    @staticmethod
    def render_welcome_message():
        """Render welcome message jika tidak ada chat history"""
        if len(st.session_state.messages) == 0:
            st.info("""
            👋 **Selamat datang di IMDB Movie Assistant!**
            
            Saya dapat membantu Anda menemukan film berdasarkan:
            - 🎬 Judul film
            - ⭐ Rating IMDB
            - 🎭 Aktor/Aktris
            - 📅 Tahun rilis
            - 🎪 Genre
            
            Silakan tanyakan apa saja tentang film dari dataset IMDB Top 1000!
            
            **Contoh pertanyaan:**
            - "Rekomendasikan film action terbaik"
            - "Film apa saja yang dibintangi Tom Hanks?"
            - "Cari film drama dengan rating di atas 8.5"
            - "Film sci-fi terbaik tahun 1990an"
            """)


class ChatInterface:
    """Class untuk mengelola chat interface"""
    
    @staticmethod
    def get_user_input() -> str:
        """
        Dapatkan input dari user melalui chat input
        
        Returns:
            User input string atau None
        """
        return st.chat_input(
            "Tanyakan tentang film, aktor, sutradara, genre..."
        )
    
    @staticmethod
    def display_user_message(message: str):
        """
        Tampilkan user message di chat
        
        Args:
            message: Pesan dari user
        """
        with st.chat_message("user"):
            st.markdown(message)
    
    @staticmethod
    def display_ai_message(message: str):
        """
        Tampilkan AI message di chat
        
        Args:
            message: Pesan dari AI
        """
        with st.chat_message("assistant"):
            st.markdown(message)
    
    @staticmethod
    def display_ai_thinking():
        """Tampilkan indikator netral saat AI berpikir"""
        messages = [
            "💭 Memproses permintaan Anda... / Processing your request...",
            "🔍 Menganalisis informasi yang relevan... / Analyzing relevant information...",
            "🧠 Mencari jawaban terbaik... / Searching for the best answer...",
            "⚙️ Mengambil informasi dari basis data... / Retrieving information from the database...",
            "💡 Menyiapkan respons yang akurat... / Preparing an accurate response..."
        ]
        msg = random.choice(messages)
        return st.spinner(msg)