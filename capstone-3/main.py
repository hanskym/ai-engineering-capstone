"""
Main application file untuk IMDB Movie Recommendation Agent
"""
import streamlit as st

from config import Config
from services import initialize_services
from tools import create_movie_tools
from agent import MovieRecommendationAgent
from utils import SessionStateManager
from ui_components import UIComponents, ChatInterface


def main():
    """Fungsi utama aplikasi"""
    
    # Setup page configuration
    UIComponents.setup_page_config()
    
    # Load dan validasi API keys
    api_keys = Config.load_api_keys()
    
    if not Config.validate_api_keys(api_keys):
        st.error("❌ API keys tidak lengkap!")
        st.info("""
        Pastikan Anda memiliki file `.env` atau Streamlit secrets dengan:
        - OPENAI_API_KEY
        - QDRANT_URL
        - QDRANT_API_KEY
        """)
        st.stop()
    
    # Inisialisasi services
    llm, embeddings, vector_store = initialize_services(api_keys)
    
    # Buat tools untuk agent
    tools = create_movie_tools(vector_store)
    
    # Inisialisasi agent
    if "agent" not in st.session_state:
        st.session_state.agent = MovieRecommendationAgent(
            llm=llm,
            tools=tools,
            language="indonesian"
        )
    
    agent = st.session_state.agent
    
    # Inisialisasi session state
    SessionStateManager.initialize()
    
    # Render UI components
    UIComponents.render_header()
    UIComponents.render_sidebar()
    
    # Tampilkan welcome message jika belum ada chat
    UIComponents.render_welcome_message()
    
    # Render chat history
    UIComponents.render_chat_history()
    
    # Handle user input
    if prompt := ChatInterface.get_user_input():
        # Tampilkan user message
        ChatInterface.display_user_message(prompt)
        SessionStateManager.add_message("user", prompt)
        
        # Process dengan agent
        with ChatInterface.display_ai_thinking():
            response = agent.process_query(prompt)
        
        # Tampilkan AI response
        if response["success"]:
            ChatInterface.display_ai_message(response["answer"])
            SessionStateManager.add_message("assistant", response["answer"])
            
            # Update costs
            SessionStateManager.update_costs(
                response["usd_price"],
                response["idr_price"]
            )
            
            # Tampilkan metrics
            UIComponents.render_response_metrics(response)
        else:
            st.error(response["answer"])
    
    # Render footer
    UIComponents.render_footer()


if __name__ == "__main__":
    main()