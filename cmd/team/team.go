package team

import (
	"fmt"
	"os"

	"github.com/1Doomdie1/Tines-CLI/cmd/team/member"
	"github.com/1Doomdie1/Tines-CLI/pkg"

	"github.com/spf13/cobra"
)

var TeamCmd = &cobra.Command{
	Use:   "team",
	Short: "Manage teams",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		if !pkg.IsTenantSet() {
			fmt.Println("fatal: No tenant set.")
			fmt.Println("Recomanded commands")
			fmt.Println("   -> tines tenant checkout -d <DOMAIN>                      |   checkout tenant")
			os.Exit(1)
		}
		cmd.Help()
	},
}

func init() {
	TeamCmd.AddCommand(TeamListCmd)
	TeamCmd.AddCommand(TeamCreateCmd)
	TeamCmd.AddCommand(TeamUpdateCmd)
	TeamCmd.AddCommand(member.MemberCmd)
}
