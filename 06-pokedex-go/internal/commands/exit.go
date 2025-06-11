package commands

import (
	"fmt"
	"os"
)

func init() {
	RegisterCommand("exit", Command{
		Name:        "exit",
		Description: "Exit the Pokedex",
		Callback:    Exit,
	})
}

// Exit handles the exit command
func Exit() error {
	fmt.Println("Closing the Pokedex... Goodbye!")
	os.Exit(0)
	return nil
}
