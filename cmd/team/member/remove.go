package member

import (
	"fmt"
	"os"

	"github.com/1Doomdie1/Tines-CLI/pkg"
	"github.com/spf13/cobra"
)

var MemberRemoveCmd = &cobra.Command{
	Use:   "remove",
	Short: "Remove member from team",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		teamId, _ := cmd.Flags().GetInt("team-id")
		userId, _ := cmd.Flags().GetInt("user-id")

		if err := pkg.RemoveTeamMember(teamId, userId); err != nil {
			fmt.Printf("fatal: %v", err)
			os.Exit(1)
		}
		fmt.Print("Member sucessfully removed")
	},
}

func init() {
	MemberRemoveCmd.Flags().IntP("team-id", "t", 0, "Team ID")
	MemberRemoveCmd.Flags().IntP("user-id", "u", 0, "User ID")

	if err := MemberRemoveCmd.MarkFlagRequired("team-id"); err != nil {
		fmt.Println(err)
	}

	if err := MemberRemoveCmd.MarkFlagRequired("user-id"); err != nil {
		fmt.Println(err)
	}
}
