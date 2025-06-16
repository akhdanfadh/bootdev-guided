package pokeapi

import (
	"testing"
	"time"
)

func TestAddGet(t *testing.T) {
	tests := []struct {
		name string
		key  string
		val  []byte
	}{
		{
			name: "simple URL",
			key:  "https://example.com",
			val:  []byte("testdata"),
		},
		{
			name: "empty value",
			key:  "empty-key",
			val:  []byte{},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			cache := NewCache(5 * time.Second)
			cache.Add(tt.key, tt.val)
			val, ok := cache.Get(tt.key)
			if !ok {
				t.Errorf("expected to find key")
				return
			}
			if string(val) != string(tt.val) {
				t.Errorf("expected to find value")
				return
			}
		})
	}
}

func TestReapLoop(t *testing.T) {
	const baseTime = 1 * time.Second
	const waitTime = baseTime + 1*time.Second
	cache := NewCache(baseTime)
	cache.Add("https://example.com", []byte("testdata"))

	_, ok := cache.Get("https://example.com")
	if !ok {
		t.Errorf("expected to find key")
		return
	}

	time.Sleep(waitTime)

	_, ok = cache.Get("https://example.com")
	if ok {
		t.Errorf("expected to not find key")
		return
	}
}

func TestGetNonExistent(t *testing.T) {
	tests := []struct {
		name string
		key  string
	}{
		{
			name: "never added key",
			key:  "non-existent-key",
		},
		{
			name: "empty string key",
			key:  "",
		},
		{
			name: "special characters key",
			key:  "!@#$%^&*()",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			cache := NewCache(5 * time.Second)
			val, ok := cache.Get(tt.key)
			if ok {
				t.Errorf("expected not to find non-existent key")
			}
			if val != nil {
				t.Errorf("expected nil value for non-existent key, got %v", val)
			}
		})
	}
}

func TestCacheOverwrite(t *testing.T) {
	tests := []struct {
		name     string
		key      string
		initial  []byte
		updated  []byte
		expected string
	}{
		{
			name:     "overwrite with different value",
			key:      "https://example.com",
			initial:  []byte("initial"),
			updated:  []byte("updated"),
			expected: "updated",
		},
		{
			name:     "overwrite with empty value",
			key:      "test-key",
			initial:  []byte("something"),
			updated:  []byte{},
			expected: "",
		},
		{
			name:     "overwrite empty with value",
			key:      "another-key",
			initial:  []byte{},
			updated:  []byte("new-value"),
			expected: "new-value",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			cache := NewCache(5 * time.Second)
			cache.Add(tt.key, tt.initial)
			cache.Add(tt.key, tt.updated)

			val, ok := cache.Get(tt.key)
			if !ok {
				t.Errorf("expected to find key")
				return
			}

			if string(val) != tt.expected {
				t.Errorf("expected %s, got %s", tt.expected, string(val))
			}
		})
	}
}
