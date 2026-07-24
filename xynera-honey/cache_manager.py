"""
cache_manager.py

Optimized Smart Filesystem Cache Management
Performance-focused implementation
"""

import time
from typing import Dict, List, Optional, Set, Any
from collections import defaultdict, OrderedDict
from dataclasses import dataclass, field
import threading
import hashlib
import json
import sys


@dataclass
class CacheEntry:
    """Individual cache entry with metadata"""
    data: Any
    timestamp: float = field(default_factory=time.time)
    ttl: Optional[float] = None
    access_count: int = 0
    last_access: float = field(default_factory=time.time)
    size: int = 0
    
    def is_expired(self) -> bool:
        if self.ttl is None:
            return False
        return (time.time() - self.timestamp) > self.ttl
    
    def touch(self):
        self.last_access = time.time()
        self.access_count += 1


class CacheManager:
    """
    Performance-Optimized Smart Cache Manager
    
    Optimizations:
    - Uses OrderedDict for O(1) LRU operations
    - Dependency tracking with set operations
    - Thread-safe with RLock
    - Fast key generation with caching
    """
    
    def __init__(self, max_size: int = 2000, default_ttl: Optional[float] = 300):
        self._cache: Dict[str, CacheEntry] = {}
        self._access_order: OrderedDict = OrderedDict()  # For LRU tracking
        self._dependencies: Dict[str, Set[str]] = defaultdict(set)
        self._reverse_deps: Dict[str, Set[str]] = defaultdict(set)
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._lock = threading.RLock()
        self._key_cache: Dict[str, str] = {}  # Cache for key generation
        self._stats = {
            "hits": 0,
            "misses": 0,
            "invalidations": 0,
            "evictions": 0,
            "memory_usage": 0,
            "entries": 0
        }
        
    def _generate_key(self, *args, **kwargs) -> str:
        """Fast key generation with caching"""
        # Create a string representation
        key_parts = []
        for arg in args:
            if isinstance(arg, (dict, list)):
                key_parts.append(json.dumps(arg, sort_keys=True))
            else:
                key_parts.append(str(arg))
        
        for k, v in sorted(kwargs.items()):
            if isinstance(v, (dict, list)):
                key_parts.append(f"{k}:{json.dumps(v, sort_keys=True)}")
            else:
                key_parts.append(f"{k}:{v}")
        
        combined = "|".join(key_parts)
        
        # Cache the key generation
        if combined in self._key_cache:
            return self._key_cache[combined]
        
        key = hashlib.md5(combined.encode()).hexdigest()
        # Only cache if key is not too large
        if len(combined) < 1000:
            self._key_cache[combined] = key
            # Limit key cache size
            if len(self._key_cache) > 10000:
                self._key_cache.clear()
        
        return key
    
    def get(self, key: str, default: Any = None, touch: bool = True) -> Any:
        """Fast retrieval with LRU update"""
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                if entry.is_expired():
                    self._invalidate(key)
                    self._stats["misses"] += 1
                    return default
                
                if touch:
                    entry.touch()
                    # Update access order for LRU
                    self._access_order.move_to_end(key)
                
                self._stats["hits"] += 1
                return entry.data
            
            self._stats["misses"] += 1
            return default
    
    def set(self, key: str, value: Any, ttl: Optional[float] = None, 
            dependencies: Optional[List[str]] = None):
        """Fast store with LRU eviction"""
        with self._lock:
            # Quick size check
            if len(self._cache) >= self._max_size:
                self._evict_lru()
            
            # Calculate size
            size = sys.getsizeof(value) if value is not None else 0
            
            entry = CacheEntry(
                data=value,
                ttl=ttl or self._default_ttl,
                size=size
            )
            
            # Remove old entry if exists
            old_entry = self._cache.get(key)
            if old_entry:
                self._stats["memory_usage"] -= old_entry.size
                self._remove_dependencies(key)
                if key in self._access_order:
                    del self._access_order[key]
            
            self._cache[key] = entry
            self._access_order[key] = None
            self._stats["memory_usage"] += size
            self._stats["entries"] = len(self._cache)
            
            # Track dependencies
            if dependencies:
                for dep in dependencies:
                    self._dependencies[key].add(dep)
                    self._reverse_deps[dep].add(key)
            
            return True
    
    def invalidate(self, key: str) -> None:
        """Invalidate a specific cache entry"""
        with self._lock:
            self._invalidate(key)
    
    def invalidate_dependent(self, dependency_key: str) -> None:
        """Fast invalidation of dependent entries"""
        with self._lock:
            if dependency_key in self._reverse_deps:
                # Get affected keys
                affected = list(self._reverse_deps[dependency_key])
                for key in affected:
                    self._invalidate(key)
            
            # Also invalidate the dependency itself
            if dependency_key in self._cache:
                self._invalidate(dependency_key)
    
    def _invalidate(self, key: str) -> None:
        """Internal fast invalidation (call with lock)"""
        if key in self._cache:
            entry = self._cache.pop(key)
            self._stats["memory_usage"] -= entry.size
            self._stats["invalidations"] += 1
            self._stats["entries"] = len(self._cache)
            
            if key in self._access_order:
                del self._access_order[key]
            
            self._remove_dependencies(key)
            
            # Invalidate dependents
            if key in self._reverse_deps:
                dependents = list(self._reverse_deps[key])
                for dep_key in dependents:
                    if dep_key in self._cache:
                        self._invalidate(dep_key)
                del self._reverse_deps[key]
    
    def _remove_dependencies(self, key: str) -> None:
        """Remove dependency tracking (call with lock)"""
        if key in self._dependencies:
            deps = self._dependencies.pop(key)
            for dep in deps:
                if dep in self._reverse_deps:
                    self._reverse_deps[dep].discard(key)
    
    def _evict_lru(self) -> None:
        """Fast LRU eviction"""
        if not self._cache:
            return
        
        # Get oldest entries (first items in OrderedDict)
        evict_count = max(1, len(self._cache) // 5)
        keys_to_evict = list(self._access_order.keys())[:evict_count]
        
        for key in keys_to_evict:
            if key in self._cache:
                self._invalidate(key)
                self._stats["evictions"] += 1
    
    def clear(self) -> None:
        """Clear all cache entries"""
        with self._lock:
            self._cache.clear()
            self._access_order.clear()
            self._dependencies.clear()
            self._reverse_deps.clear()
            self._stats["memory_usage"] = 0
            self._stats["entries"] = 0
    
    def get_stats(self) -> Dict:
        """Get cache performance statistics"""
        with self._lock:
            total_requests = self._stats["hits"] + self._stats["misses"]
            hit_rate = (self._stats["hits"] / total_requests * 100) if total_requests > 0 else 0
            
            return {
                "entries": self._stats["entries"],
                "memory_usage": self._stats["memory_usage"],
                "hits": self._stats["hits"],
                "misses": self._stats["misses"],
                "hit_rate": f"{hit_rate:.2f}%",
                "invalidations": self._stats["invalidations"],
                "evictions": self._stats["evictions"],
                "dependencies": len(self._dependencies),
                "reverse_dependencies": len(self._reverse_deps)
            }
    
    def get_dependency_tree(self, key: str) -> Dict:
        """Get the dependency tree for a key (for debugging)"""
        with self._lock:
            return {
                "key": key,
                "dependencies": list(self._dependencies.get(key, set())),
                "dependents": list(self._reverse_deps.get(key, set())),
                "in_cache": key in self._cache,
                "access_count": self._cache[key].access_count if key in self._cache else 0
            }


# Global cache manager instance
_filesystem_cache = CacheManager(max_size=2000, default_ttl=300)

def get_cache_manager() -> CacheManager:
    """Get the global cache manager instance"""
    return _filesystem_cache


def cached(dependencies_key: Optional[str] = None, ttl: Optional[float] = None):
    """
    Decorator for automatic caching
    
    Args:
        dependencies_key: Key for dependency tracking
        ttl: Time to live in seconds
    """
    def decorator(func):
        cache = get_cache_manager()
        
        def wrapper(*args, **kwargs):
            # Fast key generation
            key_parts = [func.__name__]
            
            # Handle args
            for arg in args:
                if isinstance(arg, (dict, list)):
                    key_parts.append(hashlib.md5(json.dumps(arg, sort_keys=True).encode()).hexdigest())
                else:
                    key_parts.append(str(arg))
            
            # Handle kwargs
            for k, v in sorted(kwargs.items()):
                if isinstance(v, (dict, list)):
                    key_parts.append(f"{k}:{hashlib.md5(json.dumps(v, sort_keys=True).encode()).hexdigest()}")
                else:
                    key_parts.append(f"{k}:{v}")
            
            cache_key = hashlib.md5("|".join(key_parts).encode()).hexdigest()
            
            # Try cache
            cached_value = cache.get(cache_key, touch=True)
            if cached_value is not None:
                return cached_value
            
            # Compute and cache
            result = func(*args, **kwargs)
            
            deps = []
            if dependencies_key:
                deps.append(dependencies_key)
            elif args and len(args) > 0:
                # Use first argument as dependency if it's a string
                if isinstance(args[0], str):
                    deps.append(args[0])
            
            cache.set(cache_key, result, ttl=ttl, dependencies=deps if deps else None)
            return result
        
        return wrapper
    return decorator