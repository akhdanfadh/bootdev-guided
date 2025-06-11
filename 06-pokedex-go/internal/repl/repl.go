package repl

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"github.com/akhdanfadh/bootdev-guided/06-pokedex-go/internal/commands"
)

// StartRepl begins the REPL loop
func StartRepl() {
	scanner := bufio.NewScanner(os.Stdin)
	for {
		fmt.Print("Pokedex > ")
		scanner.Scan()
		words := cleanInput(scanner.Text())
		if len(words) == 0 {
			continue
		}

		command, exists := commands.GetCommand(words[0])
		if !exists {
			fmt.Println("Unknown command")
			continue
		}

		if err := command.Callback(); err != nil {
			fmt.Printf("Error: %v\n", err)
		}
		fmt.Println()
	}
}

// cleanInput processes the input string by trimming whitespace,
// converting to lowercase, and splitting into words.
func cleanInput(text string) []string {
	return strings.Fields(strings.ToLower(strings.TrimSpace(text)))
}
