package commands

// command is an interface that all commands must implement
type command interface {
	Name() string
	Description() string
	Execute(args []string) error
}

var commandRegistry = make(map[string]command)

// RegisterCommand adds a new command to the registry
func RegisterCommand(name string, cmd command) {
	commandRegistry[name] = cmd
}

// GetCommand retrieves a command from the registry by name
func GetCommand(name string) (command, bool) {
	cmd, exists := commandRegistry[name]
	return cmd, exists
}

// GetAllCommands returns all registered commands
func GetAllCommands() map[string]command {
	return commandRegistry
}
