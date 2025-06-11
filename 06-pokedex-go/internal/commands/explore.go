package commands

import (
	"errors"
	"fmt"

	"github.com/akhdanfadh/bootdev-guided/06-pokedex-go/internal/pokeapi"
)

func init() {
	RegisterCommand("explore", Command{
		Name:        "explore",
		Description: "Given location area, display all Pokemon there",
		Callback:    Explore,
	})
}

// Explore handles the explore command
func Explore(args []string) error {
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
