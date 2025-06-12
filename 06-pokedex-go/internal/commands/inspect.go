package commands

import (
	"errors"
	"fmt"
	"slices"

	"github.com/akhdanfadh/bootdev-guided/06-pokedex-go/internal/pokeapi"
)

func init() {
	RegisterCommand("inspect", Command{
		Name:        "inspect",
		Description: "Inspect a Pokemon that has been caught",
		Callback:    Inspect,
	})
}

// Inspect handles the inspect command
func Inspect(args []string) error {
	if len(args) != 1 {
		return errors.New("usage: inspect <pokemon>")
	}

	pokemonName := args[0]
	if !slices.Contains(caughtPokemon, pokemonName) {
		// TODO: second argument may not be a valid Pokemon name
		return errors.New("you have not caught that Pokemon")
	}

	var pokemon pokeapi.Pokemon
	fullUrl := pokeapi.BASE_URL + "/pokemon/" + pokemonName
	err := pokeapi.GetAndDecode(fullUrl, &pokemon)
	if err != nil {
		return err
	}

	fmt.Println("Name:", pokemon.Name)
	fmt.Println("Height:", pokemon.Height)
	fmt.Println("Weight:", pokemon.Weight)
	fmt.Println("Stats:")
	for _, ps := range pokemon.Stats {
		fmt.Printf(" - %s: %d\n", ps.Stat.Name, ps.BaseStat)
	}
	fmt.Println("Types:")
	for _, pt := range pokemon.Types {
		fmt.Printf(" - %s\n", pt.Type.Name)
	}

	return nil
}
