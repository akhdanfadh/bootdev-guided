package commands

import (
	"errors"
	"fmt"

	"github.com/akhdanfadh/bootdev-guided/06-pokedex-go/internal/pokeapi"
)

// ExploreCommand implements the explore command
type ExploreCommand struct{}

func init() {
	RegisterCommand("explore", &ExploreCommand{})
}

// Name returns the command name
func (e *ExploreCommand) Name() string {
	return "explore"
}

// Description returns the command description
func (e *ExploreCommand) Description() string {
	return "Given location area, display all Pokemon there"
}

// Execute handles the explore command execution
func (e *ExploreCommand) Execute(args []string) error {
	if len(args) != 1 {
		return errors.New("usage: explore <location area>")
	}

	var locationArea pokeapi.LocationArea
	fullUrl := pokeapi.BASE_URL + "/location-area/" + args[0]
	err := pokeapi.GetAndDecode(fullUrl, &locationArea)
	if err != nil {
		return err
	}

	fmt.Println("Exploring", locationArea.Name, "...")
	fmt.Println("Found Pokemon:")
	for _, pokemon := range locationArea.PokemonList {
		fmt.Println(" -", pokemon.Pokemon.Name)
	}
	return nil
}
