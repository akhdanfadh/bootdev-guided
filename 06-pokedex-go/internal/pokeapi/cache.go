package pokeapi

import (
	"sync"
	"time"
)

type cacheEntry struct {
	createdAt time.Time
	val       []byte
}

type Cache struct {
	entry    map[string]cacheEntry
	interval time.Duration // interval for reaping expired entries
	mu       sync.RWMutex  // optimized for read-heavy workloads, which cache are
}

// Add adds a new entry to the cache.
func (c *Cache) Add(key string, val []byte) {
	c.mu.Lock()
	defer c.mu.Unlock()

	entry := cacheEntry{
		createdAt: time.Now(),
		val:       val,
	}
	c.entry[key] = entry
}

// Get retrieves an entry from the cache.
func (c *Cache) Get(key string) ([]byte, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	entry, exists := c.entry[key]
	if !exists {
		return nil, false
	}

	return entry.val, true
}

// reapLoop periodically removes expired entries from the cache.
func (c *Cache) reapLoop() {
	// create a runtime timer that ticks/fires every c.interval nanoseconds
	// each firing sends current time to the channel ticker.C
	ticker := time.NewTicker(c.interval)
	defer ticker.Stop() // ensure ticker is stopped, preventing resource leaks

	for range ticker.C {
		c.mu.Lock()
		for key, entry := range c.entry {
			cutoff := entry.createdAt.Add(c.interval)
			if time.Now().After(cutoff) {
				delete(c.entry, key)
			}
		}
		c.mu.Unlock() // note: not defer, since inside for loop
	}
}

// NewCache creates a new Cache instance with the specified interval for reaping expired entries.
func NewCache(interval time.Duration) *Cache {
	cache := &Cache{
		entry:    make(map[string]cacheEntry),
		interval: interval,
		mu:       sync.RWMutex{},
	}
	go cache.reapLoop() // start the reap loop in the background
	return cache        // function returns, but goroutine continues
}
