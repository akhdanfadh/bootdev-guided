package config

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

const configFile = ".gatorconfig.json"

type Config struct {
	DatabaseURL     string `json:"db_url"`
	CurrentUsername string `json:"current_user_name"`
}

// Read reads the configuration from the user's home directory
func Read() (Config, error) {
	configFile, err := getConfigFilePath()
	if err != nil {
		return Config{}, err
	}
	data, err := os.ReadFile(configFile)
	if err != nil {
		return Config{}, fmt.Errorf("failed to read config file %s: %w", configFile, err)
	}
	var config Config
	if err := json.Unmarshal(data, &config); err != nil {
		return Config{}, fmt.Errorf("failed to parse config file %s: %w", configFile, err)
	}
	return config, nil
}

func (c *Config) SetUser(username string) error {
	c.CurrentUsername = username
	if err := write(*c); err != nil {
		return err
	}
	return nil
}

// getConfigFilePath constructs the path to the configuration file
func getConfigFilePath() (string, error) {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		return "", fmt.Errorf("$HOME variable is not set: %w", err)
	}
	configPath := filepath.Join(homeDir, configFile)
	if _, err := os.Stat(configPath); err != nil {
		return "", fmt.Errorf("config file does not exist at %s: %w", configPath, err)
	}
	return configPath, nil
}

// writeConfig writes/updates the configuration to the user's home directory
func write(config Config) error {
	configFile, err := getConfigFilePath()
	if err != nil {
		return err
	}
	data, err := json.Marshal(config)
	if err != nil {
		return fmt.Errorf("failed to marshal config: %w", err)
	}
	if err := os.WriteFile(configFile, data, 0644); err != nil {
		return fmt.Errorf("failed to write config file %s: %w", config, err)
	}
	return nil
}
