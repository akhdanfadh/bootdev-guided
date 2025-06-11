package commands

import "fmt"

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

	for _, command := range GetAllCommands() {
		fmt.Printf("%s: %s\n", command.Name, command.Description)
	}
	return nil
}
