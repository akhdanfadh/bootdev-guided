package main

import (
	"errors"
	"fmt"

	"github.com/akhdanfadh/bootdev-guided/07-gator-go/internal/config"
)

type state struct {
	config *config.Config
}

type command struct {
	name string
	args []string
}

type commands struct {
	handlerMap map[string]func(*state, *command) error
}

func (c *commands) run(s *state, cmd *command) error {
	handler, exists := c.handlerMap[cmd.name]
	if !exists {
		return errors.New("unknown command: " + cmd.name)
	}
	err := handler(s, cmd)
	if err != nil {
		return err
	}
	return nil
}

func (c *commands) register(name string, f func(*state, *command) error) {
	if c.handlerMap == nil {
		c.handlerMap = make(map[string]func(*state, *command) error)
	}
	c.handlerMap[name] = f
}

func handlerLogin(s *state, cmd *command) error {
	if len(cmd.args) != 1 {
		return errors.New("login command requires exactly one argument: username")
	}
	err := s.config.SetUser(cmd.args[0])
	if err != nil {
		return err
	}
	fmt.Println("Login successful for user:", cmd.args[0])
	return nil
}
