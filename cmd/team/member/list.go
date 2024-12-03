package member

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"

	"github.com/1Doomdie1/Tines-CLI/pkg"
	"github.com/aquasecurity/table"
	"github.com/spf13/cobra"
)

var MemberListCmd = &cobra.Command{
	Use:   "list",
	Short: "List team members",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {

		teamId, _ := cmd.Flags().GetInt("team-id")
		format, _ := cmd.Flags().GetString("format")

		members, err := pkg.GetTeamMembers(teamId)

		if err != nil {
			fmt.Printf("fatal: %v", err)
			os.Exit(1)
		}

		if format == "text" {
			fmt.Println("\n" +
				"########################################\n" +
				"#               Members                #\n" +
				"########################################",
			)

			for _, member := range members {
				msg := fmt.Sprintf(
					"- ID              : %v\n"+
						"- First Name      : %s\n"+
						"- Last Name       : %s\n"+
						"- Email           : %s\n"+
						"- Is Admin        : %v\n"+
						"- Created At      : %v\n"+
						"- Last Seen       : %v\n"+
						"- Accepted Invite : %v\n"+
						"- Role            : %s\n"+
						"========================================",
					member.ID,
					member.FirstName,
					member.LastName,
					member.Email,
					member.IsAdmin,
					member.CreatedAt,
					member.LastSeen,
					member.InvitationAccepted,
					member.Role,
				)
				fmt.Println(msg)
			}
		} else if format == "json" {
			d, _ := json.MarshalIndent(members, "", "  ")
			fmt.Println(string(d))
		} else if format == "table" {
			t := table.New(os.Stdout)
			t.SetHeaders("ID", "First Name", "Last Name", "Email", "Is Admin", "Created At", "Last Seen", "Accepted Invite", "Role")
			t.SetHeaderStyle(table.StyleBold)
			t.SetDividers(table.UnicodeRoundedDividers)

			for _, member := range members {
				t.AddRow(
					strconv.Itoa(member.ID),
					member.FirstName,
					member.LastName,
					member.Email,
					strconv.FormatBool(member.IsAdmin),
					member.CreatedAt,
					member.LastSeen,
					strconv.FormatBool(member.InvitationAccepted),
					member.Role,
				)
			}
			t.Render()
		} else {
			fmt.Print("fatal: format can have only these values: table & json")
			os.Exit(1)
		}
	},
}

func init() {
	MemberListCmd.Flags().IntP("team-id", "t", 0, "Team id")
	MemberListCmd.Flags().StringP("format", "r", "text", "Format output as text, json or table")

	if err := MemberListCmd.MarkFlagRequired("team-id"); err != nil {
		fmt.Println(err)
	}
}
