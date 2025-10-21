import pandas as pd
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams


class QdrantVectorDBSetup:
    """Class untuk setup vector database menggunakan Qdrant Cloud"""
    
    def __init__(self):
        self.collection_name = "imdb_movies"
        self.embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
        self.dataset_path = "dataset/imdb_top_1000.csv"
        self.batch_size = 50
        
        # Muat environment variables
        load_dotenv()
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        self.client = None
        self.embeddings = None
        self.df = None
    
    def validate_credentials(self):
        """Validasi kredensial API"""
        if not all([self.qdrant_url, self.qdrant_api_key]):
            print("❌ Error: API keys tidak ditemukan di file .env")
            print("Pastikan Anda memiliki:")
            print("  - QDRANT_URL")
            print("  - QDRANT_API_KEY")
            return False
        
        print("✅ API keys berhasil dimuat\n")
        return True
    
    def initialize_qdrant_client(self):
        """Inisialisasi koneksi ke Qdrant Cloud"""
        print("Menghubungkan ke Qdrant Cloud...")
        try:
            self.client = QdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_api_key,
                prefer_grpc=False
            )
            print("✅ Koneksi berhasil\n")
            return True
        except Exception as e:
            print(f"❌ Gagal terhubung ke Qdrant: {str(e)}")
            return False
    
    def handle_existing_collection(self):
        """Cek dan handle collection yang sudah ada"""
        try:
            existing_collection = self.client.get_collection(self.collection_name)
            print(f"⚠️  Collection '{self.collection_name}' sudah ada")
            user_input = input("Apakah Anda ingin menghapus dan membuat ulang? (yes/no): ").lower()
            
            if user_input == 'yes':
                print(f"Menghapus collection '{self.collection_name}'...")
                self.client.delete_collection(self.collection_name)
                print("✅ Collection berhasil dihapus\n")
                return True
            else:
                print("Operasi dibatalkan")
                return False
        except Exception:
            print(f"Collection belum ada. Akan membuat yang baru.\n")
            return True
    
    def initialize_embeddings(self):
        """Inisialisasi HuggingFace embeddings (gratis, lokal, 384 dimensi)"""
        print("Menginisialisasi HuggingFace embeddings...")
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True}
            )
            print("✅ Embeddings berhasil diinisialisasi\n")
            return True
        except Exception as e:
            print(f"❌ Gagal menginisialisasi embeddings: {str(e)}")
            return False
    
    def load_dataset(self):
        """Muat dataset IMDB"""
        print("Memuat dataset IMDB...")
        try:
            self.df = pd.read_csv(self.dataset_path)
            print(f"✅ Dataset berhasil dimuat: {len(self.df)} film")
            print("\nKolom dataset:", self.df.columns.tolist())
            print("\nContoh data baris pertama:")
            print(self.df.iloc[0])
            return True
        except FileNotFoundError:
            print(f"❌ Error: {self.dataset_path} tidak ditemukan")
            print("Silakan download dataset dan letakkan di folder dataset/")
            return False
        except Exception as e:
            print(f"❌ Error memuat dataset: {str(e)}")
            return False
    
    def prepare_documents(self):
        """Siapkan dokumen untuk embedding"""
        print("\n📝 Menyiapkan dokumen untuk embedding...")
        documents = []
        
        for idx, row in self.df.iterrows():
            # Handle nilai NaN
            title = str(row.get('Series_Title', 'N/A'))
            year = str(row.get('Released_Year', 'N/A'))
            genre = str(row.get('Genre', 'N/A'))
            rating = str(row.get('IMDB_Rating', 'N/A'))
            director = str(row.get('Director', 'N/A'))
            overview = str(row.get('Overview', 'N/A'))
            runtime = str(row.get('Runtime', 'N/A'))
            certificate = str(row.get('Certificate', 'N/A'))
            
            # Ambil daftar bintang film
            stars = []
            for i in range(1, 5):
                star = row.get(f'Star{i}', None)
                if pd.notna(star):
                    stars.append(str(star))
            stars_str = ", ".join(stars) if stars else "N/A"
            
            # Gabungkan semua informasi untuk embedding
            content = f"""
Movie Title: {title}
Release Year: {year}
Genre: {genre}
IMDB Rating: {rating}
Director: {director}
Stars: {stars_str}
Runtime: {runtime}
Certificate: {certificate}
Overview: {overview}
            """.strip()
            
            # Buat document dengan metadata
            doc = Document(
                page_content=content,
                metadata={
                    "title": title,
                    "year": int(year) if year.isdigit() else 0,
                    "rating": float(rating) if rating.replace('.', '').isdigit() else 0.0,
                    "genre": genre,
                    "director": director,
                    "stars": stars_str,
                    "source": "IMDB"
                }
            )
            documents.append(doc)
            
            # Indikator progress
            if (idx + 1) % 100 == 0:
                print(f"  Diproses {idx + 1}/{len(self.df)} dokumen")
        
        print(f"✅ Total dokumen yang disiapkan: {len(documents)}\n")
        return documents
    
    def create_vector_store(self, documents):
        """Buat vector store dan upload dokumen ke Qdrant Cloud"""
        print("🚀 Membuat vector database di Qdrant Cloud...")
        print("Proses ini mungkin memakan waktu beberapa menit untuk 1000 dokumen...\n")
        
        try:
            vector_store = QdrantVectorStore.from_documents(
                documents,
                embedding=self.embeddings,
                url=self.qdrant_url,
                api_key=self.qdrant_api_key,
                collection_name=self.collection_name,
                prefer_grpc=False,
                batch_size=self.batch_size
            )
            
            print("✅ Vector database berhasil dibuat!")
            return vector_store
        except Exception as e:
            print(f"❌ Error membuat vector database: {str(e)}")
            print("\nPanduan troubleshooting:")
            print("1. Cek apakah QDRANT_URL benar (tanpa https://)")
            print("2. Cek apakah QDRANT_API_KEY valid")
            print("3. Cek apakah file dataset ada di dataset/imdb_top_1000.csv")
            return None
    
    def display_collection_info(self):
        """Tampilkan informasi collection"""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            print(f"\n📊 Statistik Collection:")
            print(f"  - Nama Collection: {self.collection_name}")
            print(f"  - Jumlah Vector: {collection_info.points_count}")
            
            # Handle struktur atribut yang berbeda
            try:
                if hasattr(collection_info.config.params.vectors, 'size'):
                    vector_size = collection_info.config.params.vectors.size
                elif isinstance(collection_info.config.params.vectors, dict):
                    vector_size = collection_info.config.params.vectors.get('size', 'unknown')
                else:
                    vector_size = collection_info.config.params.vectors.vectors.size if hasattr(
                        collection_info.config.params.vectors, 'vectors') else 'unknown'
                print(f"  - Dimensi Vector: {vector_size}")
            except Exception:
                print(f"  - Dimensi Vector: 384 (HuggingFace all-MiniLM-L6-v2)")
        except Exception as e:
            print(f"⚠️  Tidak dapat mengambil info collection: {str(e)}")
    
    def run(self):
        """Jalankan seluruh proses setup"""
        print("="*50)
        print("SETUP VECTOR DATABASE - IMDB MOVIES")
        print("="*50 + "\n")
        
        # Validasi kredensial
        if not self.validate_credentials():
            return False
        
        # Inisialisasi Qdrant client
        if not self.initialize_qdrant_client():
            return False
        
        # Handle collection yang sudah ada
        if not self.handle_existing_collection():
            return False
        
        # Inisialisasi embeddings
        if not self.initialize_embeddings():
            return False
        
        # Muat dataset
        if not self.load_dataset():
            return False
        
        # Siapkan dokumen
        documents = self.prepare_documents()
        if not documents:
            print("❌ Tidak ada dokumen yang disiapkan")
            return False
        
        # Buat vector store
        vector_store = self.create_vector_store(documents)
        if not vector_store:
            return False
        
        # Tampilkan info collection
        self.display_collection_info()
        
        print("\n" + "="*50)
        print("✅ SETUP SELESAI!")
        print("="*50)
        print("\nAnda sekarang dapat menjalankan aplikasi Streamlit:")
        print("  streamlit run main.py")
        
        return True


if __name__ == "__main__":
    setup = QdrantVectorDBSetup()
    success = setup.run()
    
    if not success:
        exit(1)