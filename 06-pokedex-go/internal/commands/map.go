package commands

import (
	"errors"
	"fmt"
)

var mapState struct {
	Next     string
	Previous string
}

func init() {
	mapState.Next = BASE_URL + "/location-area?limit=20"
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
	var locationAreas NamedApiResourceList
	if mapState.Next == "" {
		return errors.New("end of entries")
	}
	err := getAndDecode(mapState.Next, &locationAreas)
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
	var locationAreas NamedApiResourceList
	if mapState.Previous == "" {
		return errors.New("no earlier entries")
	}
	err := getAndDecode(mapState.Previous, &locationAreas)
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
