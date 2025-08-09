"""
Test suite for the advanced search cache functionality.
Tests the SimpleTTLCache, SimpleLRUCache, and SearchCache classes.
"""
import time
from unittest.mock import MagicMock

import pytest

from src import models
from src.services.search_cache import SearchCache, SimpleLRUCache, SimpleTTLCache


class TestSimpleTTLCache:
    """Test the TTL (Time-To-Live) cache implementation."""

    def test_basic_get_set(self):
        """Test basic cache operations."""
        cache = SimpleTTLCache(maxsize=10, ttl=60)
        
        # Create mock search response
        mock_response = MagicMock(spec=models.SearchResponse)
        
        # Test set and get
        cache.set("test_key", mock_response)
        result = cache.get("test_key")
        assert result == mock_response
        
        # Test non-existent key
        assert cache.get("nonexistent") is None

    def test_ttl_expiration(self):
        """Test that items expire after TTL."""
        cache = SimpleTTLCache(maxsize=10, ttl=1)  # 1 second TTL
        
        mock_response = MagicMock(spec=models.SearchResponse)
        cache.set("test_key", mock_response)
        
        # Should be available immediately
        assert cache.get("test_key") == mock_response
        
        # Wait for expiration
        time.sleep(1.1)
        
        # Should be expired
        assert cache.get("test_key") is None

    def test_maxsize_eviction(self):
        """Test that oldest items are evicted when maxsize is reached."""
        cache = SimpleTTLCache(maxsize=2, ttl=60)
        
        mock_response1 = MagicMock(spec=models.SearchResponse)
        mock_response2 = MagicMock(spec=models.SearchResponse)
        mock_response3 = MagicMock(spec=models.SearchResponse)
        
        cache.set("key1", mock_response1)
        cache.set("key2", mock_response2)
        cache.set("key3", mock_response3)  # Should evict key1
        
        assert cache.get("key1") is None  # Evicted
        assert cache.get("key2") == mock_response2
        assert cache.get("key3") == mock_response3

    def test_clear(self):
        """Test cache clearing."""
        cache = SimpleTTLCache(maxsize=10, ttl=60)
        
        mock_response = MagicMock(spec=models.SearchResponse)
        cache.set("test_key", mock_response)
        
        assert cache.get("test_key") == mock_response
        
        cache.clear()
        assert cache.get("test_key") is None

    def test_len_with_expiration(self):
        """Test that __len__ cleans up expired entries."""
        cache = SimpleTTLCache(maxsize=10, ttl=1)
        
        mock_response = MagicMock(spec=models.SearchResponse)
        cache.set("test_key", mock_response)
        
        assert len(cache) == 1
        
        time.sleep(1.1)
        assert len(cache) == 0  # Should clean up expired entry


class TestSimpleLRUCache:
    """Test the LRU (Least Recently Used) cache implementation."""

    def test_basic_get_set(self):
        """Test basic cache operations."""
        cache = SimpleLRUCache(maxsize=10)
        
        mock_quote = MagicMock(spec=models.Quote)
        
        cache.set("test_key", mock_quote)
        result = cache.get("test_key")
        assert result == mock_quote
        
        assert cache.get("nonexistent") is None

    def test_lru_eviction(self):
        """Test LRU eviction behavior."""
        cache = SimpleLRUCache(maxsize=2)
        
        mock_quote1 = MagicMock(spec=models.Quote)
        mock_quote2 = MagicMock(spec=models.Quote)
        mock_quote3 = MagicMock(spec=models.Quote)
        
        cache.set("key1", mock_quote1)
        cache.set("key2", mock_quote2)
        
        # Access key1 to make it most recently used
        cache.get("key1")
        
        # Add key3, should evict key2 (least recently used)
        cache.set("key3", mock_quote3)
        
        assert cache.get("key1") == mock_quote1  # Still present
        assert cache.get("key2") is None  # Evicted
        assert cache.get("key3") == mock_quote3

    def test_update_existing(self):
        """Test updating existing keys."""
        cache = SimpleLRUCache(maxsize=10)
        
        mock_quote1 = MagicMock(spec=models.Quote)
        mock_quote2 = MagicMock(spec=models.Quote)
        
        cache.set("key1", mock_quote1)
        cache.set("key1", mock_quote2)  # Update
        
        assert cache.get("key1") == mock_quote2
        assert len(cache) == 1

    def test_clear(self):
        """Test cache clearing."""
        cache = SimpleLRUCache(maxsize=10)
        
        mock_quote = MagicMock(spec=models.Quote)
        cache.set("test_key", mock_quote)
        
        assert len(cache) == 1
        cache.clear()
        assert len(cache) == 0


class TestSearchCache:
    """Test the advanced SearchCache functionality."""

    def create_mock_quote(self, symbol: str, longname: str = None) -> models.Quote:
        """Create a mock quote for testing."""
        raw_data = MagicMock()
        raw_data.symbol = symbol
        raw_data.longname = longname
        
        quote = MagicMock(spec=models.Quote)
        quote.raw = raw_data
        return quote

    def create_search_response(self, query: str, quotes: list) -> models.SearchResponse:
        """Create a mock search response for testing."""
        search_query = models.SearchQuery(query=query)
        return models.SearchResponse(query=search_query, quotes=quotes)

    def test_exact_cache_hit(self):
        """Test exact query matching from cache."""
        cache = SearchCache(max_size=10, ttl=60)
        
        quote = self.create_mock_quote("AAPL", "Apple Inc.")
        response = self.create_search_response("apple", [quote])
        
        # Cache the response
        cache.set("apple", response)
        
        # Should get exact match
        result = cache.get("apple")
        assert result is not None
        assert result.query.query == "apple"
        assert len(result.quotes) == 1

    def test_case_insensitive_matching(self):
        """Test case-insensitive query matching."""
        cache = SearchCache(max_size=10, ttl=60)
        
        quote = self.create_mock_quote("AAPL", "Apple Inc.")
        response = self.create_search_response("Apple", [quote])
        
        cache.set("Apple", response)
        
        # Should match regardless of case
        assert cache.get("apple") is not None
        assert cache.get("APPLE") is not None
        assert cache.get("ApPlE") is not None

    def test_ticker_caching_for_partial_matches(self):
        """Test that individual tickers are cached for partial matching."""
        cache = SearchCache(max_size=10, ttl=60)
        
        apple_quote = self.create_mock_quote("AAPL", "Apple Inc.")
        microsoft_quote = self.create_mock_quote("MSFT", "Microsoft Corporation")
        
        response = self.create_search_response("tech stocks", [apple_quote, microsoft_quote])
        
        # Cache the response
        cache.set("tech stocks", response)
        
        # Now search for just "apple" - should find partial match
        result = cache.get("apple")
        assert result is not None
        assert len(result.quotes) == 1
        assert result.quotes[0].raw.symbol == "AAPL"

    def test_partial_match_by_company_name(self):
        """Test partial matching by company name."""
        cache = SearchCache(max_size=10, ttl=60)
        
        apple_quote = self.create_mock_quote("AAPL", "Apple Inc.")
        response = self.create_search_response("fruit company", [apple_quote])
        
        cache.set("fruit company", response)
        
        # Search by company name part
        result = cache.get("inc")
        assert result is not None
        assert len(result.quotes) == 1
        assert result.quotes[0].raw.symbol == "AAPL"

    def test_duplicate_removal_in_partial_matches(self):
        """Test that duplicate tickers are removed in partial matches."""
        cache = SearchCache(max_size=10, ttl=60)
        
        apple_quote = self.create_mock_quote("AAPL", "Apple Inc.")
        
        # Cache the same ticker under different queries
        response1 = self.create_search_response("apple", [apple_quote])
        response2 = self.create_search_response("tech", [apple_quote])
        
        cache.set("apple", response1)
        cache.set("tech", response2)
        
        # Search should return only one instance
        result = cache.get("fruit tech")  # Should match both cached queries
        assert result is not None
        assert len(result.quotes) == 1  # No duplicates
        assert result.quotes[0].raw.symbol == "AAPL"

    def test_partial_match_result_limit(self):
        """Test that partial matches are limited to 10 results."""
        cache = SearchCache(max_size=100, ttl=60)
        
        # Create 15 different quotes
        quotes = [self.create_mock_quote(f"TICK{i}", f"Company {i}") for i in range(15)]
        response = self.create_search_response("companies", quotes)
        
        cache.set("companies", response)
        
        # Partial match should be limited to 10
        result = cache.get("company")
        assert result is not None
        assert len(result.quotes) <= 10

    def test_cache_stats(self):
        """Test cache statistics."""
        cache = SearchCache(max_size=10, ttl=60)
        
        apple_quote = self.create_mock_quote("AAPL", "Apple Inc.")
        response = self.create_search_response("apple", [apple_quote])
        
        # Initially empty
        stats = cache.get_stats()
        assert stats["exact_cache_size"] == 0
        assert stats["ticker_cache_size"] == 0
        assert stats["query_patterns"] == 0
        
        # After caching
        cache.set("apple", response)
        stats = cache.get_stats()
        assert stats["exact_cache_size"] == 1
        assert stats["ticker_cache_size"] >= 1  # At least the ticker symbol
        assert stats["query_patterns"] == 1

    def test_cache_clear(self):
        """Test clearing all caches."""
        cache = SearchCache(max_size=10, ttl=60)
        
        apple_quote = self.create_mock_quote("AAPL", "Apple Inc.")
        response = self.create_search_response("apple", [apple_quote])
        
        cache.set("apple", response)
        
        # Verify data is cached
        assert cache.get("apple") is not None
        stats = cache.get_stats()
        assert stats["exact_cache_size"] > 0
        
        # Clear and verify
        cache.clear()
        assert cache.get("apple") is None
        stats = cache.get_stats()
        assert stats["exact_cache_size"] == 0
        assert stats["ticker_cache_size"] == 0
        assert stats["query_patterns"] == 0

    def test_empty_query_handling(self):
        """Test handling of empty or whitespace queries."""
        cache = SearchCache(max_size=10, ttl=60)
        
        # Empty and whitespace queries should return None
        assert cache.get("") is None
        assert cache.get("   ") is None
        assert cache.get("\t\n") is None

    def test_query_normalization(self):
        """Test that queries are properly normalized."""
        cache = SearchCache(max_size=10, ttl=60)
        
        apple_quote = self.create_mock_quote("AAPL", "Apple Inc.")
        response = self.create_search_response("  Apple  ", [apple_quote])
        
        cache.set("  Apple  ", response)
        
        # Should match normalized versions
        assert cache.get("apple") is not None
        assert cache.get("Apple") is not None
        assert cache.get("  apple  ") is not None