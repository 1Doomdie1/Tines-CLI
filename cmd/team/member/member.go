package member

import (
	"github.com/spf13/cobra"
)

var MemberCmd = &cobra.Command{
	Use:   "member",
	Short: "Manage team members",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		cmd.Help()
	},
}

func init() {
	MemberCmd.AddCommand(MemberListCmd)
	MemberCmd.AddCommand(MemberRemoveCmd)
	MemberCmd.AddCommand(MemberInviteCmd)
}
