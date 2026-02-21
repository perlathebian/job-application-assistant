import hashlib
import numpy as np
from typing import Optional


class EmbeddingCache:
    """In-memory cache for sentence embeddings"""
    
    def __init__(self, max_size: int = 500):
        self._cache = {}
        self._max_size = max_size
    
    def _make_key(self, text: str) -> str:
        """Generate a unique key from text"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def get(self, text: str) -> Optional[np.ndarray]:
        """Get embedding from cache"""
        key = self._make_key(text)
        return self._cache.get(key, None)
    
    def set(self, text: str, embedding: np.ndarray) -> None:
        """Store embedding in cache"""
        # Evict oldest entry if cache is full
        if len(self._cache) >= self._max_size:
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        
        key = self._make_key(text)
        self._cache[key] = embedding
    
    def clear(self) -> None:
        """Clear all cached embeddings"""
        self._cache = {}
    
    @property
    def size(self) -> int:
        """Return current cache size"""
        return len(self._cache)