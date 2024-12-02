package team

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/1Doomdie1/Tines-CLI/pkg"

	"github.com/aquasecurity/table"
	"github.com/spf13/cobra"
)

var TeamListCmd = &cobra.Command{
	Use:   "list",
	Short: "List tenant teams",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		teams, err := pkg.TeamList()
		format, _ := cmd.Flags().GetString("format")

		if err != nil {
			fmt.Printf("fatal: %v", err)
			os.Exit(1)
		}

		if format == "json" {
			d, _ := json.MarshalIndent(teams, "", "  ")
			fmt.Println(string(d))
		} else if format == "table" {
			t := table.New(os.Stdout)
			t.SetHeaders("Team ID", "Team Name", "Groups")
			t.SetHeaderStyle(table.StyleBold)
			t.SetDividers(table.UnicodeRoundedDividers)

			for _, team := range teams.Teams {
				var groupDetails string
				if len(team.Groups) > 0 {
					for _, group := range team.Groups {
						groupDetails += fmt.Sprintf("[%d] %s\n", group.ID, group.Name)
					}
				} else {
					groupDetails = "No Groups"
				}

				t.AddRow(fmt.Sprintf("%d", team.ID), team.Name, groupDetails)
			}

			t.Render()

		} else {
			fmt.Print("fatal: format can have only these values: table & json")
			os.Exit(1)
		}

	},
}

func init() {
	TeamListCmd.Flags().StringP("format", "r", "table", "Format output as text, json or table")
}
