"""
Utility functions untuk aplikasi
"""
from config import Config


class TokenUsageCalculator:
    """Calculator untuk menghitung token usage dan cost"""
    
    def __init__(self):
        self.input_price = Config.INPUT_TOKEN_PRICE_USD
        self.output_price = Config.OUTPUT_TOKEN_PRICE_USD
        self.usd_to_idr = Config.USD_TO_IDR
    
    def calculate_usage(self, messages: list) -> dict:
        """
        Hitung total token usage dan cost dari messages
        
        Args:
            messages: List of messages dari LLM
            
        Returns:
            Dictionary berisi input_tokens, output_tokens, usd_price, idr_price
        """
        total_input_tokens = 0
        total_output_tokens = 0
        
        for message in messages:
            if hasattr(message, "response_metadata"):
                # Try usage_metadata format (newer)
                if "usage_metadata" in message.response_metadata:
                    metadata = message.response_metadata["usage_metadata"]
                    total_input_tokens += metadata.get("input_tokens", 0)
                    total_output_tokens += metadata.get("output_tokens", 0)
                # Try token_usage format (older)
                elif "token_usage" in message.response_metadata:
                    metadata = message.response_metadata["token_usage"]
                    total_input_tokens += metadata.get("prompt_tokens", 0)
                    total_output_tokens += metadata.get("completion_tokens", 0)
        
        # Hitung cost
        usd_price = (
            total_input_tokens * self.input_price + 
            total_output_tokens * self.output_price
        ) / 1_000_000
        
        idr_price = usd_price * self.usd_to_idr
        
        return {
            "input_tokens": total_input_tokens,
            "output_tokens": total_output_tokens,
            "usd_price": usd_price,
            "idr_price": idr_price
        }


class SessionStateManager:
    """Manager untuk Streamlit session state"""
    
    @staticmethod
    def initialize():
        """Inisialisasi session state variables"""
        import streamlit as st
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "total_cost_usd" not in st.session_state:
            st.session_state.total_cost_usd = 0.0
        
        if "total_cost_idr" not in st.session_state:
            st.session_state.total_cost_idr = 0.0
        
        if "total_queries" not in st.session_state:
            st.session_state.total_queries = 0
    
    @staticmethod
    def add_message(role: str, content: str):
        """Tambahkan message ke session state"""
        import streamlit as st
        st.session_state.messages.append({
            "role": role,
            "content": content
        })
    
    @staticmethod
    def update_costs(usd_cost: float, idr_cost: float):
        """Update total costs di session state"""
        import streamlit as st
        st.session_state.total_cost_usd += usd_cost
        st.session_state.total_cost_idr += idr_cost
        st.session_state.total_queries += 1
    
    @staticmethod
    def clear_history():
        """Clear chat history"""
        import streamlit as st
        st.session_state.messages = []
        st.session_state.total_cost_usd = 0.0
        st.session_state.total_cost_idr = 0.0
        st.session_state.total_queries = 0


def format_currency(amount: float, currency: str = "IDR") -> str:
    """
    Format angka menjadi currency string
    
    Args:
        amount: Jumlah uang
        currency: "IDR" atau "USD"
        
    Returns:
        Formatted string
    """
    if currency == "IDR":
        return f"Rp {amount:,.2f}"
    else:
        return f"${amount:.6f}"


def format_large_number(number: int) -> str:
    """
    Format angka besar dengan separator
    
    Args:
        number: Angka yang akan diformat
        
    Returns:
        Formatted string
    """
    return f"{number:,}"