package commands

// BASE_URL is the base URL for the PokeAPI (no trailing slash)
const BASE_URL string = "https://pokeapi.co/api/v2"

// NamedApiResource is a struct that represents a named PokeAPI resource
type NamedApiResource struct {
	Name string `json:"name"`
	Url  string `json:"url"`
}

// NamedApiResourceList is a struct that represents a list of named PokeAPI resources
type NamedApiResourceList struct {
	Count    int                `json:"count"`
	Next     string             `json:"next"`
	Previous string             `json:"previous"`
	Results  []NamedApiResource `json:"results"`
}
