package pokeapi

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

// Global cache instance with 5 minute expiration
var apiCache = NewCache(5 * time.Minute)

// getAndDecode is a helper function to get a JSON response from a URL and decode it into a struct
func GetAndDecode[T any](url string, v *T) error {
	// Check cache first
	if cachedData, found := apiCache.Get(url); found {
		// Check if this is a cached 404 response
		var errorCheck map[string]any
		if err := json.Unmarshal(cachedData, &errorCheck); err == nil {
			if status, ok := errorCheck["status"].(float64); ok && status == 404 {
				return fmt.Errorf("resource not found (404)")
			}
		}
		// Otherwise, unmarshal the cached data normally
		return json.Unmarshal(cachedData, v)
	}

	// Cache miss - make HTTP request
	res, err := http.Get(url)
	if err != nil {
		return err
	}
	defer res.Body.Close()

	body, err := io.ReadAll(res.Body)
	if err != nil {
		return err
	}

	switch res.StatusCode {
	case http.StatusOK:
		// Cache successful response
		if err := json.Unmarshal(body, v); err != nil {
			return err
		}
		apiCache.Add(url, body)
		return nil
	case http.StatusNotFound:
		// Cache 404 responses to avoid repeated lookups for non-existent resources
		apiCache.Add(url, []byte(`{"error":"not found","status":404}`))
		return fmt.Errorf("resource not found (404)")
	default:
		// Don't cache other error statuses (5xx, etc.) - allow retries
		return fmt.Errorf("API request failed with status %d", res.StatusCode)
	}
}
