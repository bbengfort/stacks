package main

import (
	"log"
	"os"

	"github.com/bbengfort/stacks/api"
	"github.com/joho/godotenv"
	"gopkg.in/urfave/cli.v1"
)

func main() {
	// Load the .env file if it exists
	godotenv.Load()

	// Instantiate the command line application
	app := cli.NewApp()
	app.Name = "stacks"
	app.Version = api.PackageVersion
	app.Usage = "run and manage the stacks API server"

	// Define commands available to the application
	app.Commands = []cli.Command{
		{
			Name:     "serve",
			Usage:    "run the stacks API server",
			Action:   serve,
			Category: "server",
			Flags: []cli.Flag{
				cli.BoolFlag{
					Name:   "d, debug",
					Usage:  "run the server in debug mode",
					EnvVar: "STACKS_DEBUG",
				},
				cli.StringFlag{
					Name:   "a, addr",
					Usage:  "host and port to listen on",
					EnvVar: "STACKS_ADDR",
					Value:  ":8080",
				},
			},
		},
	}

	// Run the CLI program
	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}

//===========================================================================
// Server Commands
//===========================================================================

func serve(c *cli.Context) (err error) {
	if err := api.Serve(c.String("addr"), c.Bool("debug")); err != nil {
		return cli.NewExitError(err, 1)
	}
	return nil
}
