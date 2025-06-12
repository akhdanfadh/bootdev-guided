package commands

import (
	"errors"
	"fmt"
	"math"
	"math/rand"

	"github.com/akhdanfadh/bootdev-guided/06-pokedex-go/internal/pokeapi"
)

// CatchCommand implements the catch command
type CatchCommand struct {
	caughtPokemon *[]string
}

var sharedCaughtPokemon = &[]string{}

func init() {
	RegisterCommand("catch", &CatchCommand{caughtPokemon: sharedCaughtPokemon})
}

// Name returns the command name
func (c *CatchCommand) Name() string {
	return "catch"
}

// Description returns the command description
func (c *CatchCommand) Description() string {
	return "Attempt to catch a Pokemon"
}

// catch is a helper function to catch a Pokemon based on its base experience.
// It uses a sigmoid function with pre-calculated parameters based on overall
// base experiences to calculate the catch probability for individual Pokemon.
func (c *CatchCommand) catch(pokemon pokeapi.Pokemon) bool {
	// Calculate the individual catch probability
	sigmoidParams := pokeapi.GetCatchPokemonParams()
	catchProb := 1 / (1 + math.Exp(sigmoidParams.Steepness*(float64(pokemon.BaseExperience)-sigmoidParams.Midpoint)))

	// Pokemon caught if a random number is less than probability
	randomRoll := rand.Float64() // between 0 and 1
	return randomRoll < catchProb
}

// Execute handles the catch command execution
func (c *CatchCommand) Execute(args []string) error {
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
	if c.catch(pokemon) {
		fmt.Printf("%s was caught!\n", pokemon.Name)
		*c.caughtPokemon = append(*c.caughtPokemon, pokemon.Name)
	} else {
		fmt.Printf("%s escaped!\n", pokemon.Name)
	}

	return nil
}
