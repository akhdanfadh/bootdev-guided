package commands

import (
	"fmt"
	"sort"
)

func init() {
	RegisterCommand("help", Command{
		Name:        "help",
		Description: "Displays a help message",
		Callback:    Help,
	})
}

// Help handles the help command
func Help(args []string) error {
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
		fmt.Printf("%s: %s\n", commands[k].Name, commands[k].Description)
	}
	return nil
}
