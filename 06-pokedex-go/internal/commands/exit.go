package commands

import (
	"fmt"
	"os"
)

// ExitCommand implements the exit command
type ExitCommand struct{}

func init() {
	RegisterCommand("exit", &ExitCommand{})
}

// Name returns the command name
func (e *ExitCommand) Name() string {
	return "exit"
}

// Description returns the command description
func (e *ExitCommand) Description() string {
	return "Exit the Pokedex"
}

// Execute handles the exit command execution
func (e *ExitCommand) Execute(args []string) error {
	fmt.Println("Closing the Pokedex... Goodbye!")
	os.Exit(0)
	return nil
}
