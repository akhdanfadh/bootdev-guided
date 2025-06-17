package main

import (
	"fmt"
	"os"

	"github.com/akhdanfadh/bootdev-guided/07-gator-go/internal/config"
)

func main() {
	// Parse command line arguments
	args := os.Args[1:]
	if len(args) == 0 {
		fmt.Println("no arguments provided")
		os.Exit(1)
	}

	// Read configuration from the user's home directory
	config, err := config.Read()
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	println("Configuration loaded before modification:")
	println("Database URL:", config.DatabaseURL)
	println("Current Username:", config.CurrentUsername)
	println()

	// Register state and commands
	state := state{config: &config}
	commands := commands{}
	commands.register("login", handlerLogin)

	// Run the command from arguments
	command := command{name: args[0], args: args[1:]}
	err = commands.run(&state, &command)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	println()
	println("Configuration updated after modification:")
	println("Database URL:", config.DatabaseURL)
	println("Current Username:", config.CurrentUsername)
}
