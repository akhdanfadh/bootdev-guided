package pokeapi

import (
	"encoding/json"
	"fmt"
	"net/http"
)

// getAndDecode is a helper function to get a JSON response from a URL and decode it into a struct
func GetAndDecode[T any](url string, v *T) error {
	res, err := http.Get(url)
	if err != nil {
		return err
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		return fmt.Errorf("API request failed with status %d", res.StatusCode)
	}

	if err := json.NewDecoder(res.Body).Decode(v); err != nil {
		return err
	}
	return nil
}
