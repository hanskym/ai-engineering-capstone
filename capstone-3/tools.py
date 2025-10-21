"""
Tools untuk RAG agent - fungsi pencarian film
"""
from langchain.tools import tool
from config import Config


def create_movie_tools(vector_store):
    """
    Factory function untuk membuat movie search tools
    
    Args:
        vector_store: QdrantVectorStore instance
        
    Returns:
        List of tools
    """
    k = Config.DEFAULT_SEARCH_K
    
    @tool
    def search_movies(query: str) -> str:
        """
        Cari film di database IMDB berdasarkan judul, genre, sutradara, aktor, tahun, atau rating.
        Query akan otomatis mencari di semua field yang relevan.
        
        Args:
            query: Kata kunci pencarian (contoh: "Tom Hanks", "action movie", "1994", "Toy Story")
            
        Returns:
            String berisi informasi film yang ditemukan
        """
        try:
            results = vector_store.similarity_search(query, k=k)
            
            if not results:
                return "Tidak ada film yang ditemukan untuk query tersebut."
            
            # Format hasil pencarian
            formatted_results = []
            for idx, doc in enumerate(results, 1):
                formatted_results.append(f"Film {idx}:\n{doc.page_content}\n")
            
            return "\n".join(formatted_results)
        except Exception as e:
            return f"Error saat mencari film: {str(e)}"
    
    return [search_movies]