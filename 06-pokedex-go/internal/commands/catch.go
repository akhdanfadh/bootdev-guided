package commands

import (
	"errors"
	"fmt"
	"math"
	"math/rand"

	"github.com/akhdanfadh/bootdev-guided/06-pokedex-go/internal/pokeapi"
)

func init() {
	RegisterCommand("catch", Command{
		Name:        "catch",
		Description: "Attempt to catch a Pokemon",
		Callback:    Catch,
	})
}

// catch is a helper function to catch a Pokemon based on its base experience.
// It uses a sigmoid function with pre-calculated parameters based on overall
// base experiences to calculate the catch probability for individual Pokemon.
func catch(pokemon pokeapi.Pokemon) bool {
	// Calculate the individual catch probability
	sigmoidParams := pokeapi.GetCatchPokemonParams()
	catchProb := 1 / (1 + math.Exp(sigmoidParams.Steepness*(float64(pokemon.BaseExperience)-sigmoidParams.Midpoint)))

	// Pokemon caught if a random number is less than probability
	randomRoll := rand.Float64() // between 0 and 1
	return randomRoll < catchProb
}

// Catch handles the catch command
func Catch(args []string) error {
	if len(args) != 1 {
		return errors.New("usage: catch <pokemon>")
	}

	fullUrl := pokeapi.BASE_URL + "/pokemon/" + args[0]
	var pokemon pokeapi.Pokemon
	err := pokeapi.GetAndDecode(fullUrl, &pokemon)
	if err != nil {
		return err
	}

	fmt.Printf("Throwing a Pokeball at %s...\n", pokemon.Name)
	if catch(pokemon) {
		fmt.Printf("%s was caught!\n", pokemon.Name)
	} else {
		fmt.Printf("%s escaped!\n", pokemon.Name)
	}

	return nil
}
