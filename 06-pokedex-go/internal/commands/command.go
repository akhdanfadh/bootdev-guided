package commands

// Command represents a CLI command with its name, description, and callback function
type Command struct {
	Name        string
	Description string
	Callback    func(args []string) error
}

var registry = make(map[string]Command)

// RegisterCommand adds a new command to the registry
func RegisterCommand(name string, cmd Command) {
	registry[name] = cmd
}

// GetCommand retrieves a command from the registry by name
func GetCommand(name string) (Command, bool) {
	cmd, exists := registry[name]
	return cmd, exists
}

// GetAllCommands returns all registered commands
func GetAllCommands() map[string]Command {
	return registry
}
