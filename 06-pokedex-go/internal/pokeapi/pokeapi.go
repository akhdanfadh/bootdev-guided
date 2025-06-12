package pokeapi

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

// Pokemon is a struct that represents a Pokemon
type Pokemon struct {
	Id             int    `json:"id"`
	Name           string `json:"name"`
	BaseExperience int    `json:"base_experience"`
}

// CatchPokemonParams is the sigmoid parameters for catching Pokemon.
type CatchPokemonParams struct {
	Midpoint  float64
	Steepness float64
}

// GetCatchPokemonParams returns the sigmoid parameters for catching Pokemon.
// This is a "constant" variable that is used to calculate the catch probability.
// For validation, the minimum base experience is 36 and maximum is 608.
func GetCatchPokemonParams() CatchPokemonParams {
	return CatchPokemonParams{
		Midpoint:  172.0,
		Steepness: 0.0183321,
	}
}
