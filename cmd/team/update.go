package team

import (
	"fmt"
	"os"

	"github.com/1Doomdie1/Tines-CLI/pkg"

	"github.com/spf13/cobra"
)

var TeamUpdateCmd = &cobra.Command{
	Use:   "update",
	Short: "Update team",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {

		name, _ := cmd.Flags().GetString("name")
		teamId, _ := cmd.Flags().GetInt("team-id")

		if err := pkg.UpdateTeam(name, teamId); err != nil {
			fmt.Printf("fatal: %s", err)
			os.Exit(1)
		}
		fmt.Println("Team name updated")
	},
}

func init() {
	TeamUpdateCmd.Flags().StringP("name", "n", "", "New team name")
	TeamUpdateCmd.Flags().IntP("team-id", "t", 0, "Team id")

	if err := TeamUpdateCmd.MarkFlagRequired("name"); err != nil {
		fmt.Println(err)
	}

	if err := TeamUpdateCmd.MarkFlagRequired("team-id"); err != nil {
		fmt.Println(err)
	}
}
