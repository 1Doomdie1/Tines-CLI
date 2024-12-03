package workflow

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"

	"github.com/1Doomdie1/Tines-CLI/pkg"
	"github.com/1Doomdie1/Tines-CLI/utils"
	"github.com/aquasecurity/table"
	"github.com/spf13/cobra"
)

var filterChoices = []string{
	"LOCKED",
	"FAVORITE",
	"DISABLED",
	"PUBLISHED",
	"API_ENABLED",
	"ALL_STORIES",
	"HIGH_PRIORITY",
	"WORKBENCH_ENABLED",
	"SEND_TO_STORY_ENABLED",
	"CHANGE_CONTROL_ENABLED",
}

var orderChoices = []string{
	"NAME",
	"NAME_DESC",
	"RECENTLY_EDITED",
	"ACTION_COUNT_ASC",
	"ACTION_COUNT_DESC",
	"LEAST_RECENTLY_EDITED",
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

		if !utils.IsStringInArray(filter, filterChoices) {
			fmt.Printf("fatal: invalid filter value '%s'. Valid options are: %s\n", filter, strings.Join(filterChoices, ", "))
			os.Exit(1)
		}

		if !utils.IsStringInArray(order, orderChoices) {
			fmt.Printf("fatal: invalid order value '%s'. Valid options are: %s\n", order, strings.Join(orderChoices, ", "))
			os.Exit(1)
		}

		if format != "text" && format != "json" && format != "table" {
			fmt.Printf("fatal: invalid format value '%s'. Valid options are: text, json & table\n", format)
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
		} else if format == "table" {
			t := table.New(os.Stdout)
			t.SetHeaders("ID", "Name", "Team ID", "Folder ID", "Disabled", "Priority", "Published", "Edited At", "Created At", "Updated At", "GUID")
			t.SetHeaderStyle(table.StyleBold)
			t.SetDividers(table.UnicodeRoundedDividers)

			for _, workflow := range workflows {
				t.AddRow(
					strconv.Itoa(workflow.ID),
					workflow.Name,
					strconv.Itoa(workflow.TeamID),
					strconv.Itoa(workflow.FolderID),
					strconv.FormatBool(workflow.Disabled),
					strconv.FormatBool(workflow.Priority),
					strconv.FormatBool(workflow.Published),
					workflow.EditedAt,
					workflow.CreatedAt,
					workflow.UpdatedAt,
					workflow.GUID,
				)
			}

			t.Render()

		} else if format == "json" {
			jsonData, err := json.MarshalIndent(workflows, "", "  ")

			if err != nil {
				fmt.Println("fatal:", err)
				os.Exit(1)
			}

			fmt.Println(string(jsonData))
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
