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

// LocationArea is a struct that represents a location area and its Pokemon encounters
type LocationArea struct {
	Id          int    `json:"id"`
	Name        string `json:"name"`
	PokemonList []struct {
		Pokemon struct {
			Name string `json:"name"`
			Url  string `json:"url"`
		} `json:"pokemon"`
	} `json:"pokemon_encounters"`
}
