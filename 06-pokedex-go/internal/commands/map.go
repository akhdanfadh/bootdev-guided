package commands

import (
	"errors"
	"fmt"

	"github.com/akhdanfadh/bootdev-guided/06-pokedex-go/internal/pokeapi"
)

// MapCommand implements the map command
type MapCommand struct {
	state *mapStateData
}

// MapBackCommand implements the mapb command
type MapBackCommand struct {
	state *mapStateData
}

// mapStateData holds the shared state for map navigation
type mapStateData struct {
	Next     string
	Previous string
}

var sharedMapState = &mapStateData{
	Next:     pokeapi.BASE_URL + "/location-area?limit=20",
	Previous: "",
}

func init() {
	RegisterCommand("map", &MapCommand{state: sharedMapState})
	RegisterCommand("mapb", &MapBackCommand{state: sharedMapState})
}

// Name returns the command name
func (m *MapCommand) Name() string {
	return "map"
}

// Description returns the command description
func (m *MapCommand) Description() string {
	return "Display the next 20 location areas"
}

// Execute handles the map command execution
func (m *MapCommand) Execute(args []string) error {
	var locationAreas pokeapi.LocationAreaList
	if m.state.Next == "" {
		return errors.New("end of entries")
	}
	err := pokeapi.GetAndDecode(m.state.Next, &locationAreas)
	if err != nil {
		return err
	}

	m.state.Next = locationAreas.Next
	m.state.Previous = locationAreas.Previous

	for _, locationArea := range locationAreas.Results {
		fmt.Println(locationArea.Name)
	}

	return nil
}

// Name returns the command name
func (mb *MapBackCommand) Name() string {
	return "mapb"
}

// Description returns the command description
func (mb *MapBackCommand) Description() string {
	return "Display the previous 20 location areas"
}

// Execute handles the mapb command execution
func (mb *MapBackCommand) Execute(args []string) error {
	var locationAreas pokeapi.LocationAreaList
	if mb.state.Previous == "" {
		return errors.New("no earlier entries")
	}
	err := pokeapi.GetAndDecode(mb.state.Previous, &locationAreas)
	if err != nil {
		return err
	}

	mb.state.Next = locationAreas.Next
	mb.state.Previous = locationAreas.Previous

	for _, locationArea := range locationAreas.Results {
		fmt.Println(locationArea.Name)
	}

	return nil
}
