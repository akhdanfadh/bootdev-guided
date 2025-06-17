package main

import (
	"os"

	"github.com/akhdanfadh/bootdev-guided/07-gator-go/internal/config"
)

func main() {
	config, err := config.Read()
	if err != nil {
		print(err)
		os.Exit(1)
	}

	println("Configuration loaded before modification:")
	println("Database URL:", config.DatabaseURL)
	println("Current Username:", config.CurrentUsername)

	username := "gator_user"
	err = config.SetUser(username)
	if err != nil {
		print(err)
		os.Exit(1)
	}

	println("Configuration updated after modification:")
	println("Database URL:", config.DatabaseURL)
	println("Current Username:", config.CurrentUsername)
}
