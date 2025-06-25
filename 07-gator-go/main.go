package main

import (
	"database/sql"
	"fmt"
	"os"

	"github.com/akhdanfadh/bootdev-guided/07-gator-go/internal/config"
	"github.com/akhdanfadh/bootdev-guided/07-gator-go/internal/database"
	_ "github.com/lib/pq"
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

	println("Initial configuration:")
	println("Database URL:", config.DatabaseURL)
	println("Current Username:", config.CurrentUsername)
	println()

	// Open a connection to the database
	db, err := sql.Open("postgres", config.DatabaseURL)
	if err != nil {
		fmt.Println("failed to connect to database:", err)
		os.Exit(1)
	}
	defer db.Close()

	// Create a new database queries instance
	dbQueries := database.New(db)

	// Register state and commands
	state := state{
		db:  dbQueries,
		cfg: &config,
	}
	commands := commands{}
	commands.register("login", handlerLogin)
	commands.register("register", handlerRegister)
	commands.register("reset", handlerReset)

	// Run the command from arguments
	command := command{name: args[0], args: args[1:]}
	err = commands.run(&state, &command)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	println()
	println("Updated configuration:")
	println("Database URL:", config.DatabaseURL)
	println("Current Username:", config.CurrentUsername)
}
