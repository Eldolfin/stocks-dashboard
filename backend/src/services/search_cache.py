"""
Advanced caching service for stock search results.
Provides intelligent caching with fuzzy matching and result merging.
"""
import time
from typing import Dict, List, Optional, Set, Tuple
from src import models


class SimpleTTLCache:
    """Simple time-to-live cache implementation."""
    
    def __init__(self, maxsize: int, ttl: int):
        self.maxsize = maxsize
        self.ttl = ttl
        self._cache: Dict[str, Tuple[models.SearchResponse, float]] = {}
    
    def get(self, key: str) -> Optional[models.SearchResponse]:
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, value: models.SearchResponse) -> None:
        # Remove oldest entries if at capacity
        while len(self._cache) >= self.maxsize:
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
            del self._cache[oldest_key]
        
        self._cache[key] = (value, time.time())
    
    def clear(self) -> None:
        self._cache.clear()
    
    def __len__(self) -> int:
        # Clean expired entries
        current_time = time.time()
        expired_keys = [k for k, (_, timestamp) in self._cache.items() 
                       if current_time - timestamp >= self.ttl]
        for key in expired_keys:
            del self._cache[key]
        return len(self._cache)


class SimpleLRUCache:
    """Simple least-recently-used cache implementation."""
    
    def __init__(self, maxsize: int):
        self.maxsize = maxsize
        self._cache: Dict[str, models.Quote] = {}
        self._order: List[str] = []
    
    def get(self, key: str) -> Optional[models.Quote]:
        if key in self._cache:
            # Move to end (most recently used)
            self._order.remove(key)
            self._order.append(key)
            return self._cache[key]
        return None
    
    def set(self, key: str, value: models.Quote) -> None:
        if key in self._cache:
            # Update existing
            self._order.remove(key)
        elif len(self._cache) >= self.maxsize:
            # Remove least recently used
            oldest = self._order.pop(0)
            del self._cache[oldest]
        
        self._cache[key] = value
        self._order.append(key)
    
    def clear(self) -> None:
        self._cache.clear()
        self._order.clear()
    
    def __len__(self) -> int:
        return len(self._cache)
    
    def items(self):
        return self._cache.items()


class SearchCache:
    """Advanced search cache with intelligent result merging and fuzzy matching."""
    
    def __init__(self, max_size: int = 1000, ttl: int = 600):
        # Main cache for exact query matches
        self._exact_cache = SimpleTTLCache(maxsize=max_size, ttl=ttl)
        
        # Cache for individual ticker results to enable partial matches
        self._ticker_cache = SimpleLRUCache(maxsize=max_size * 2)
        
        # Track query patterns for smarter caching
        self._query_patterns: Dict[str, Set[str]] = {}
        
    def get(self, query: str) -> Optional[models.SearchResponse]:
        """Get cached search results for a query."""
        query_normalized = query.strip().lower()
        
        # Try exact match first
        result = self._exact_cache.get(query_normalized)
        if result:
            return result
        
        # Try to build result from cached tickers if query is subset
        partial_result = self._try_partial_match(query_normalized)
        if partial_result:
            return partial_result
            
        return None
    
    def set(self, query: str, result: models.SearchResponse) -> None:
        """Cache search results and individual tickers."""
        query_normalized = query.strip().lower()
        
        # Cache the full result
        self._exact_cache.set(query_normalized, result)
        
        # Cache individual tickers for partial matching
        for quote in result.quotes:
            ticker_key = quote.raw.symbol.lower()
            company_key = (quote.raw.longname or "").lower()
            
            self._ticker_cache.set(ticker_key, quote)
            if company_key:
                self._ticker_cache.set(company_key, quote)
        
        # Track query patterns
        query_words = set(query_normalized.split())
        for word in query_words:
            if word not in self._query_patterns:
                self._query_patterns[word] = set()
            self._query_patterns[word].add(query_normalized)
    
    def _try_partial_match(self, query: str) -> Optional[models.SearchResponse]:
        """Try to build results from cached tickers for partial matches."""
        query_words = query.split()
        matched_tickers = []
        
        # Look for tickers that match any word in the query
        for word in query_words:
            word_lower = word.lower()
            
            # Check direct ticker matches
            for cached_key, ticker in self._ticker_cache.items():
                if (word_lower in cached_key or 
                    any(word_lower in (ticker.raw.longname or "").lower().split())):
                    matched_tickers.append(ticker)
        
        if matched_tickers:
            # Remove duplicates while preserving order
            unique_tickers = []
            seen_symbols = set()
            for ticker in matched_tickers:
                if ticker.raw.symbol not in seen_symbols:
                    unique_tickers.append(ticker)
                    seen_symbols.add(ticker.raw.symbol)
            
            # Limit results to avoid overwhelming
            unique_tickers = unique_tickers[:10]
            
            return models.SearchResponse(
                quotes=unique_tickers,
                query=models.SearchQuery(query=query)
            )
        
        return None
    
    def clear(self) -> None:
        """Clear all cached data."""
        self._exact_cache.clear()
        self._ticker_cache.clear()
        self._query_patterns.clear()
    
    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            "exact_cache_size": len(self._exact_cache),
            "ticker_cache_size": len(self._ticker_cache),
            "query_patterns": len(self._query_patterns),
        }


# Global cache instance
search_cache = SearchCache()