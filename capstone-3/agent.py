"""
Movie recommendation agent menggunakan LangGraph
"""
from datetime import datetime
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, ToolMessage

from prompts import MovieAgentPrompts
from utils import TokenUsageCalculator


class MovieRecommendationAgent:
    """Agent untuk rekomendasi film menggunakan RAG"""
    
    def __init__(self, llm, tools, language: str = "english"):
        """
        Inisialisasi agent
        
        Args:
            llm: Language model instance
            tools: List of tools untuk agent
            language: Bahasa untuk system prompt ("english" atau "indonesian")
        """
        self.llm = llm
        self.tools = tools
        self.language = language
        self.calculator = TokenUsageCalculator()
        
        # Pilih prompt sesuai bahasa
        if language == "indonesian":
            self.system_prompt = MovieAgentPrompts.get_indonesian_system_prompt()
        else:
            self.system_prompt = MovieAgentPrompts.get_system_prompt()
        
        # Buat agent
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.system_prompt
        )
    
    def process_query(self, question: str) -> dict:
        """
        Proses query user dengan agent
        
        Args:
            question: Pertanyaan dari user
            
        Returns:
            Dictionary berisi answer, usage, dan metadata
        """
        try:
            # Jalankan agent
            result = self.agent.invoke({
                "messages": [HumanMessage(content=question)]
            })
            
            # Extract jawaban
            answer = result["messages"][-1].content
            
            # Hitung token usage dan cost
            usage_data = self.calculator.calculate_usage(result["messages"])
            
            # Extract tool messages
            tool_messages = self._extract_tool_messages(result["messages"])
            
            return {
                "answer": answer,
                "idr_price": usage_data["idr_price"],
                "usd_price": usage_data["usd_price"],
                "total_input_tokens": usage_data["input_tokens"],
                "total_output_tokens": usage_data["output_tokens"],
                "tool_messages": tool_messages,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "success": True
            }
            
        except Exception as e:
            return {
                "answer": f"❌ Error: {str(e)}",
                "idr_price": 0,
                "usd_price": 0,
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "tool_messages": [],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "success": False
            }
    
    def _extract_tool_messages(self, messages: list) -> list:
        """
        Extract tool messages dari list messages
        
        Args:
            messages: List of messages dari agent
            
        Returns:
            List of tool message contents
        """
        tool_messages = []
        for message in messages:
            if isinstance(message, ToolMessage):
                tool_messages.append(message.content)
        return tool_messages
    
    def change_language(self, language: str):
        """
        Ubah bahasa system prompt
        
        Args:
            language: "english" atau "indonesian"
        """
        self.language = language
        
        if language == "indonesian":
            self.system_prompt = MovieAgentPrompts.get_indonesian_system_prompt()
        else:
            self.system_prompt = MovieAgentPrompts.get_system_prompt()
        
        # Recreate agent dengan prompt baru
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.system_prompt
        )