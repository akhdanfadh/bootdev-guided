package commands

import (
	"errors"
	"fmt"

	"github.com/akhdanfadh/bootdev-guided/06-pokedex-go/internal/pokeapi"
)

var mapState struct {
	Next     string
	Previous string
}

func init() {
	mapState.Next = pokeapi.BASE_URL + "/location-area?limit=20"
	mapState.Previous = ""

	RegisterCommand("map", Command{
		Name:        "map",
		Description: "Display the next 20 location areas",
		Callback:    Map,
	})

	RegisterCommand("mapb", Command{
		Name:        "mapb",
		Description: "Display the previous 20 location areas",
		Callback:    MapB,
	})
}

// Map handles the map command
func Map(args []string) error {
	var locationAreas pokeapi.LocationAreaList
	if mapState.Next == "" {
		return errors.New("end of entries")
	}
	err := pokeapi.GetAndDecode(mapState.Next, &locationAreas)
	if err != nil {
		return err
	}

	mapState.Next = locationAreas.Next
	mapState.Previous = locationAreas.Previous

	for _, locationArea := range locationAreas.Results {
		fmt.Println(locationArea.Name)
	}

	return nil
}

// MapB handles the mapb command
func MapB(args []string) error {
	var locationAreas pokeapi.LocationAreaList
	if mapState.Previous == "" {
		return errors.New("no earlier entries")
	}
	err := pokeapi.GetAndDecode(mapState.Previous, &locationAreas)
	if err != nil {
		return err
	}

	mapState.Next = locationAreas.Next
	mapState.Previous = locationAreas.Previous

	for _, locationArea := range locationAreas.Results {
		fmt.Println(locationArea.Name)
	}

	return nil
}
