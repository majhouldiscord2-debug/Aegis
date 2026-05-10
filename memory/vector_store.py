import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    """High-performance semantic retrieval using sentence-transformers with caching."""
    
    def __init__(self, model_name='all-MiniLM-L6-v2', storage_path="brain_data/vector_store.json"):
        self.model_name = model_name
        self._model = None # Lazy load
        self.storage_path = storage_path
        self.cache_path = storage_path.replace(".json", "_cache.npy")
        self.entries = self._load()
        self._embedding_cache = self._load_cache()

    @property
    def model(self):
        if self._model is None:
            print(f"DEBUG: Loading Semantic Memory Model ({self.model_name})...")
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def _load(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                return json.load(f)
        return []

    def _load_cache(self):
        if os.path.exists(self.cache_path):
            return np.load(self.cache_path)
        return np.array([])

    def _save(self):
        with open(self.storage_path, "w") as f:
            json.dump(self.entries, f, indent=4)
        if self._embedding_cache.size > 0:
            np.save(self.cache_path, self._embedding_cache)

    def add_text(self, text, metadata=None):
        """Embed and store text with metadata and cache embedding."""
        embedding = self.model.encode(text)
        self.entries.append({
            "text": text,
            "metadata": metadata or {}
        })
        
        if self._embedding_cache.size == 0:
            self._embedding_cache = np.array([embedding])
        else:
            self._embedding_cache = np.vstack([self._embedding_cache, embedding])
            
        self._save()

    def query(self, query_text, limit=3):
        """Find top-k semantically similar fragments using cached embeddings."""
        if not self.entries or self._embedding_cache.size == 0:
            return []
            
        query_embedding = self.model.encode(query_text)
        
        # Vectorized cosine similarity
        norm_query = np.linalg.norm(query_embedding)
        norm_cache = np.linalg.norm(self._embedding_cache, axis=1)
        dot_product = np.dot(self._embedding_cache, query_embedding)
        
        similarities = dot_product / (norm_query * norm_cache)
        
        top_indices = np.argsort(similarities)[::-1][:limit]
        return [self.entries[i]["text"] for i in top_indices if similarities[i] > 0.3]
