package team

import (
	"fmt"
	"os"

	"github.com/1Doomdie1/Tines-CLI/pkg"

	"github.com/spf13/cobra"
)

var TeamCreateCmd = &cobra.Command{
	Use:   "create",
	Short: "Create team",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		name, _ := cmd.Flags().GetString("name")
		if err := pkg.TeamCreate(name); err != nil {
			fmt.Printf("fatal: %s", err)
			os.Exit(1)
		}
		fmt.Print("Team has been created succesfully")
	},
}

func init() {
	TeamCreateCmd.Flags().StringP("name", "n", "", "Team name")

	if err := TeamCreateCmd.MarkFlagRequired("name"); err != nil {
		fmt.Println(err)
	}
}
