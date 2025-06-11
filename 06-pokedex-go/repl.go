package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type cliCommand struct {
	name        string
	description string
	callback    func() error
}

// Start the Pokedex REPL
func startRepl() {
	scanner := bufio.NewScanner(os.Stdin)
	for {
		// prompt and user input
		fmt.Print("Pokedex > ")
		scanner.Scan()
		words := cleanInput(scanner.Text())
		if len(words) == 0 {
			continue
		}

		// process based on command (first word)
		command, exists := getCommandRegistry()[words[0]]
		if !exists {
			fmt.Println("Unknown command")
			continue
		}
		err := command.callback()
		if err != nil {
			fmt.Println(err)
		}
	}
}

// Build and return supported commands
func getCommandRegistry() map[string]cliCommand {
	registry := make(map[string]cliCommand)
	registry["exit"] = cliCommand{
		name:        "exit",
		description: "Exit the Pokedex",
		callback:    commandExit,
	}
	registry["help"] = cliCommand{
		name:        "help",
		description: "Displays a help message",
		callback:    commandHelp,
	}
	return registry
}

// Clean user input (trim whitespace and lowercase) and split to words
func cleanInput(text string) []string {
	return strings.Fields(strings.ToLower(strings.TrimSpace(text)))
}

// Exit the program
func commandExit() error {
	fmt.Println("Closing the Pokedex... Goodbye!")
	os.Exit(0)
	return nil
}

// Prints a help message describing how to use the REPL
func commandHelp() error {
	fmt.Println("Welcome to the Pokedex!")
	fmt.Println("Usage:")
	fmt.Println()
	for _, command := range getCommandRegistry() {
		fmt.Printf("%s: %s\n", command.name, command.description)
	}
	return nil
}
