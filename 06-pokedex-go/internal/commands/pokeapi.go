package commands

// BASE_URL is the base URL for the PokeAPI (no trailing slash)
const BASE_URL string = "https://pokeapi.co/api/v2"

// LocationAreaList is a struct that represents a list of location areas
type LocationAreaList struct {
	Next     string `json:"next"`
	Previous string `json:"previous"`
	Results  []struct {
		Name string `json:"name"`
		Url  string `json:"url"`
	} `json:"results"`
}
