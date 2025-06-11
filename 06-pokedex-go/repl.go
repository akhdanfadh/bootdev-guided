package main

import "strings"

// Split the users input into "words" based on whitespace,
// lowercase the input, and trim any leading or trailing whitespace.
func cleanInput(text string) []string {
	return strings.Fields(strings.ToLower(strings.TrimSpace(text)))
}
