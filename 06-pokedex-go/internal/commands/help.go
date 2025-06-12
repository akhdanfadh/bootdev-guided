package commands

import (
	"fmt"
	"sort"
)

// HelpCommand implements the help command
type HelpCommand struct{}

func init() {
	RegisterCommand("help", &HelpCommand{})
}

// Name returns the command name
func (h *HelpCommand) Name() string {
	return "help"
}

// Description returns the command description
func (h *HelpCommand) Description() string {
	return "Displays a help message"
}

// Execute handles the help command execution
func (h *HelpCommand) Execute(args []string) error {
	fmt.Println("Welcome to the Pokedex!")
	fmt.Println("Usage:")
	fmt.Println()

	// Get all commands and sort them by key
	commands := GetAllCommands()
	keys := make([]string, 0, len(commands))
	for k := range commands {
		keys = append(keys, k)
	}
	sort.Strings(keys)

	for _, k := range keys {
		cmd := commands[k]
		fmt.Printf("%s: %s\n", cmd.Name(), cmd.Description())
	}
	return nil
}
