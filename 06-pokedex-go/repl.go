package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

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
		switch cmd := words[0]; cmd {
		case "exit":
			commandExit()
		case "help":
			commandHelp()
		default:
			fmt.Printf("Your command was: %s\n", cmd)
		}
	}
}

// Split the users input into "words" based on whitespace,
// lowercase the input, and trim any leading or trailing whitespace.
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
	fmt.Println("help: Displays a help message")
	fmt.Println("exit: Exit the Pokedex")
	return nil
}
