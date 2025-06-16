package commands

import (
	"fmt"
)

// PokedexCommand implements the pokedex command
type PokedexCommand struct {
	caughtPokemon *[]string
}

func init() {
	RegisterCommand("pokedex", &PokedexCommand{caughtPokemon: sharedCaughtPokemon})
}

// Name returns the command name
func (p *PokedexCommand) Name() string {
	return "pokedex"
}

// Description returns the command description
func (p *PokedexCommand) Description() string {
	return "Displays all caught Pokemon"
}

// Execute handles the pokedex command execution
func (p *PokedexCommand) Execute(args []string) error {
	fmt.Println("Your Pokedex:")
	for _, pokemon := range *p.caughtPokemon {
		fmt.Println(" -", pokemon)
	}
	return nil
}
