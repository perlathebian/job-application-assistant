import pytest
import numpy as np
from backend.utils.cache import EmbeddingCache


def test_cache_initialization():
    """Test cache initialization"""
    cache = EmbeddingCache(max_size=10)
    assert cache.size == 0


def test_cache_set_and_get():
    """Test setting and getting from cache"""
    cache = EmbeddingCache()
    text = "test text"
    embedding = np.array([1.0, 2.0, 3.0])
    
    cache.set(text, embedding)
    retrieved = cache.get(text)
    
    assert retrieved is not None
    assert np.array_equal(retrieved, embedding)


def test_cache_miss():
    """Test cache miss returns None"""
    cache = EmbeddingCache()
    result = cache.get("nonexistent text")
    
    assert result is None


def test_cache_eviction():
    """Test cache eviction when full"""
    cache = EmbeddingCache(max_size=2)
    
    cache.set("text1", np.array([1.0]))
    cache.set("text2", np.array([2.0]))
    cache.set("text3", np.array([3.0]))  # Should evict text1
    
    assert cache.size == 2
    assert cache.get("text1") is None  # Evicted
    assert cache.get("text2") is not None
    assert cache.get("text3") is not None


def test_cache_clear():
    """Test cache clear"""
    cache = EmbeddingCache()
    cache.set("text1", np.array([1.0]))
    cache.set("text2", np.array([2.0]))
    
    cache.clear()
    
    assert cache.size == 0
    assert cache.get("text1") is None