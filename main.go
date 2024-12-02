package main

import (
	"errors"
	"os"

	"github.com/1Doomdie1/Tines-CLI/cmd"

	"github.com/joho/godotenv"
)

func main() {
	// Create the tenants folder if it doesn't exist
	if _, err := os.Stat("tenants"); err != nil {
		if os.IsNotExist(err) {
			os.Mkdir("tenants", os.ModeDir)
		}
	}

	// Create the exports folder if it doesn't exist
	if _, err := os.Stat("exports"); err != nil {
		if os.IsNotExist(err) {
			os.Mkdir("exports", os.ModeDir)
		}
	}

	// Create .env file if it doesn't exists
	if _, err := os.Stat(".env"); errors.Is(err, os.ErrNotExist) {
		file, _ := os.Create(".env")
		defer file.Close()

		envVars := map[string]string{
			"USE_TENANT": "None",
		}
		godotenv.Write(envVars, ".env")
	}

	cmd.Execute()
}
