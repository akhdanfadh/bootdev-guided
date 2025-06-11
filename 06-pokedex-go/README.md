# Pokedex

Pokedex is a command-line [REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop) that lets us look up information about Pokemon - things like their name, type, and stats - using the incredible [PokéAPI](https://pokeapi.co/).

As `main.go` is a symlink of `cmd/pokedex/main.go`, simply run/build the project by:

```bash
# Start REPL directly
go run .

# Build the binary
go build -o pokedex
./pokedex
```

Or to build the binary

## Learning Goals

- Learn how to parse JSON in Go
- Practice making HTTP requests in Go
- Learn how to build a CLI tool that makes interacting with a back-end server easier
- Get hands-on practice with local Go development and tooling
- Learn about caching and how to use it to improve performance
