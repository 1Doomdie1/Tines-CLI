package workflow

import (
	"fmt"
	"os"
	"strings"

	"github.com/1Doomdie1/Tines-CLI/pkg"
	"github.com/spf13/cobra"
)

var filterChoices = []string{
	"ALL_STORIES",
	"SEND_TO_STORY_ENABLED",
	"WORKBENCH_ENABLED",
	"HIGH_PRIORITY",
	"API_ENABLED",
	"PUBLISHED",
	"FAVORITE",
	"CHANGE_CONTROL_ENABLED",
	"DISABLED",
	"LOCKED",
}

var orderChoices = []string{
	"NAME",
	"NAME_DESC",
	"RECENTLY_EDITED",
	"LEAST_RECENTLY_EDITED",
	"ACTION_COUNT_ASC",
	"ACTION_COUNT_DESC",
}

var WorkflowListCmd = &cobra.Command{
	Use:   "list",
	Short: "List workflows",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		teamId, _ := cmd.Flags().GetString("team-id")
		folderId, _ := cmd.Flags().GetString("folder-id")
		tags, _ := cmd.Flags().GetStringSlice("tags")
		filter, _ := cmd.Flags().GetString("filter")
		order, _ := cmd.Flags().GetString("order")
		format, _ := cmd.Flags().GetString("format")

		if !isValidChoice(filter, filterChoices) {
			fmt.Printf("fatal: invalid filter value '%s'. Valid options are: %s\n", filter, strings.Join(filterChoices, ", "))
			os.Exit(1)
		}

		if !isValidChoice(order, orderChoices) {
			fmt.Printf("fatal: invalid order value '%s'. Valid options are: %s\n", order, strings.Join(orderChoices, ", "))
			os.Exit(1)
		}

		workflows, err := pkg.ListWorkflows(teamId, folderId, tags, filter, order)

		if err != nil {
			fmt.Printf("fatal: %v", err)
			os.Exit(1)
		}

		if format == "text" {
			fmt.Printf("\n" +
				"###############################################\n" +
				"#                  Workflows                  #\n" +
				"###############################################\n",
			)

			for _, workflow := range workflows {
				msg := fmt.Sprintf(
					"- ID         : %v\n"+
						"- Name       : %s\n"+
						"- Team ID    : %v\n"+
						"- Folder ID  : %v\n"+
						"- Disabled   : %t\n"+
						"- Priority   : %t\n"+
						"- Published  : %t\n"+
						"- Edited At  : %s\n"+
						"- Created At : %s\n"+
						"- Updated At : %s\n"+
						"- GUID       : %s\n"+
						"===============================================",
					workflow.ID,
					workflow.Name,
					workflow.TeamID,
					workflow.FolderID,
					workflow.Disabled,
					workflow.Priority,
					workflow.Published,
					workflow.EditedAt,
					workflow.CreatedAt,
					workflow.UpdatedAt,
					workflow.GUID,
				)
				fmt.Println(msg)
			}

		}
	},
}

func init() {
	WorkflowListCmd.Flags().StringP("team-id", "t", "", "Team ID")
	WorkflowListCmd.Flags().StringP("folder-id", "f", "", "Folder ID")
	WorkflowListCmd.Flags().StringSlice("tags", []string{}, "Tags")
	WorkflowListCmd.Flags().StringP("filter", "i", "ALL_STORIES", fmt.Sprintf("Filters: %s", strings.Join(filterChoices, "\n\t ")))
	WorkflowListCmd.Flags().StringP("order", "o", "NAME", fmt.Sprintf("Order: %s", strings.Join(orderChoices, "\n       ")))
	WorkflowListCmd.Flags().StringP("format", "r", "text", "Format output as text, json or table")
}

func isValidChoice(value string, choices []string) bool {
	for _, choice := range choices {
		if value == choice {
			return true
		}
	}
	return false
}
