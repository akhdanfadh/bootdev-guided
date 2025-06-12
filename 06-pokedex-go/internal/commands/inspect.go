package commands

import (
	"errors"
	"fmt"
	"slices"

	"github.com/akhdanfadh/bootdev-guided/06-pokedex-go/internal/pokeapi"
)

// InspectCommand implements the inspect command
type InspectCommand struct {
	caughtPokemon *[]string
}

func init() {
	RegisterCommand("inspect", &InspectCommand{caughtPokemon: sharedCaughtPokemon})
}

// Name returns the command name
func (i *InspectCommand) Name() string {
	return "inspect"
}

// Description returns the command description
func (i *InspectCommand) Description() string {
	return "Inspect a Pokemon that has been caught"
}

// Execute handles the inspect command execution
func (i *InspectCommand) Execute(args []string) error {
	if len(args) != 1 {
		return errors.New("usage: inspect <pokemon>")
	}

	pokemonName := args[0]
	if !slices.Contains(*i.caughtPokemon, pokemonName) {
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
