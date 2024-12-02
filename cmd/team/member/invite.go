package member

import (
	"fmt"
	"os"

	"github.com/1Doomdie1/Tines-CLI/pkg"
	"github.com/spf13/cobra"
)

var validRoles = map[string]bool{
	"VIEWER":     true,
	"EDITOR":     true,
	"TEAM_ADMIN": true,
}

var MemberInviteCmd = &cobra.Command{
	Use:   "invite",
	Short: "Invite member to team",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {

		teamId, _ := cmd.Flags().GetInt("team-id")
		email, _ := cmd.Flags().GetString("email")
		role, _ := cmd.Flags().GetString("role")

		if !validRoles[role] {
			fmt.Print("fatal: role can have the following values: VIEWER, EDITOR & TEAM_ADMIN")
			os.Exit(1)
		}
		if err := pkg.InviteTeamMember(teamId, email, role); err != nil {
			fmt.Printf("fatal: %v", err)
			os.Exit(1)
		}

		fmt.Println("Invitation sent")

	},
}

func init() {
	MemberInviteCmd.Flags().IntP("team-id", "t", 0, "Team id")
	MemberInviteCmd.Flags().StringP("email", "e", "", "User email")
	MemberInviteCmd.Flags().StringP("role", "r", "VIEWER", fmt.Sprint("User roles: VIEWER\n"+
		"\t\t   EDITOR\n"+
		"\t\t   TEAM_ADMIN\n",
	))

	if err := MemberInviteCmd.MarkFlagRequired("team-id"); err != nil {
		fmt.Println(err)
	}

	if err := MemberInviteCmd.MarkFlagRequired("email"); err != nil {
		fmt.Println(err)
	}
}
