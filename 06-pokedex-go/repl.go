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
		fmt.Printf("Your command was: %s\n", words[0])
	}
}

// Split the users input into "words" based on whitespace,
// lowercase the input, and trim any leading or trailing whitespace.
func cleanInput(text string) []string {
	return strings.Fields(strings.ToLower(strings.TrimSpace(text)))
}
