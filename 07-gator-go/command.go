package main

import (
	"context"
	"errors"
	"fmt"
	"os"
	"time"

	"github.com/akhdanfadh/bootdev-guided/07-gator-go/internal/config"
	"github.com/akhdanfadh/bootdev-guided/07-gator-go/internal/database"
	"github.com/google/uuid"
)

type state struct {
	db  *database.Queries
	cfg *config.Config
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

	// make sure the user exists in the database
	user, err := s.db.GetUser(context.Background(), cmd.args[0])
	if err != nil {
		fmt.Println("failed to get user:", err)
		os.Exit(1)
	}

	// set user in config
	err = s.cfg.SetUser(user.Name)
	if err != nil {
		return err
	}
	fmt.Println("Login successful for user:", cmd.args[0])
	return nil
}

func handlerUsers(s *state, cmd *command) error {
	users, err := s.db.GetUsers(context.Background())
	if err != nil {
		return err
	}

	for _, user := range users {
		if user.Name == s.cfg.CurrentUsername {
			fmt.Println("*", user.Name, "(current)")
		} else {
			fmt.Println("*", user.Name)
		}
	}
	return nil
}

func handlerRegister(s *state, cmd *command) error {
	if len(cmd.args) != 1 {
		return errors.New("register command requires exactly one argument: username")
	}

	// create a new user in the database
	args := database.CreateUserParams{
		ID:        uuid.New(),
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
		Name:      cmd.args[0],
	}
	user, err := s.db.CreateUser(context.Background(), args)
	if err != nil {
		// since users.name is unique, the CreateUser function will return an error
		// or it can be other errors like connection error
		fmt.Println("failed to create user:", err)
		os.Exit(1)
	}

	// set current user in config
	err = s.cfg.SetUser(user.Name)
	if err != nil {
		return err
	}

	fmt.Println("User registered successfully:", user.Name)
	return nil
}

func handlerReset(s *state, cmd *command) error {
	err := s.db.DeleteAllUsers(context.Background())
	if err != nil {
		return err
	}

	fmt.Println("Database has been reset. All users are removed.")
	return nil
}

func handlerAgg(s *state, cmd *command) error {
	// currently hardcoded for bootdev submission
	feedURL := "https://www.wagslane.dev/index.xml"
	rssFeed, err := fetchFeed(context.Background(), feedURL)
	if err != nil {
		return err
	}

	printFeed(rssFeed)
	return nil
}

func handlerAddFeed(s *state, cmd *command) error {
	if len(cmd.args) != 2 {
		return errors.New("addfeed command requires exactly two arguments: feed name and feed URL")
	}

	// get current user UUID
	currentUser, err := s.db.GetUser(context.Background(), s.cfg.CurrentUsername)
	if err != nil {
		return err
	}

	// create a new feed in the database
	args := database.CreateFeedParams{
		ID:        uuid.New(),
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
		Name:      cmd.args[0],
		Url:       cmd.args[1],
		UserID:    currentUser.ID,
	}
	feed, err := s.db.CreateFeed(context.Background(), args)
	if err != nil {
		return err
	}

	// create a new feed_follows in the database
	args_new := database.CreateFeedFollowParams{
		ID:        uuid.New(),
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
		UserID:    currentUser.ID,
		FeedID:    feed.ID,
	}
	_, err = s.db.CreateFeedFollow(context.Background(), args_new)
	if err != nil {
		return err
	}

	fmt.Println("Feed added successfully:", feed.Name, "with URL of", feed.Url)
	return nil
}

func handlerFeeds(s *state, cmd *command) error {
	feeds, err := s.db.GetFeeds(context.Background())
	if err != nil {
		return err
	}

	for _, feed := range feeds {
		user, err := s.db.GetUserById(context.Background(), feed.UserID)
		if err != nil {
			return err
		}
		username := user.Name

		fmt.Printf("* %s (%s), added by %s\n", feed.Name, feed.Url, username)
	}
	return nil
}

func handlerFollow(s *state, cmd *command) error {
	if len(cmd.args) != 1 {
		return errors.New("follow command requires exactly one arguments: feed URL")
	}

	// validate the URL argument
	feed, err := s.db.GetFeedByUrl(context.Background(), cmd.args[0])
	if err != nil { // sqlc will return sql.ErrNoRows basically
		return errors.New("given feed URL does not match any feeds in the database")
	}

	// get current user UUID
	currentUser, err := s.db.GetUser(context.Background(), s.cfg.CurrentUsername)
	if err != nil {
		return err
	}

	// create a new feed_follows in the database
	args := database.CreateFeedFollowParams{
		ID:        uuid.New(),
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
		UserID:    currentUser.ID,
		FeedID:    feed.ID,
	}
	feed_follows, err := s.db.CreateFeedFollow(context.Background(), args)
	if err != nil {
		return err
	}

	fmt.Println(feed_follows.Name, "successfully follow", feed_follows.Name_2)
	return nil
}
