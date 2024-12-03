package workflow

import (
	"fmt"
	"os"
	"strings"

	"github.com/1Doomdie1/Tines-CLI/pkg"
	"github.com/1Doomdie1/Tines-CLI/utils"
	"github.com/spf13/cobra"
)

var validEventRetention = map[string]int{
	"1h":   3600,
	"6h":   21600,
	"1d":   86400,
	"3d":   259200,
	"7d":   604800,
	"14d":  1209600,
	"30d":  2592000,
	"60d":  5184000,
	"90d":  7776000,
	"180d": 15552000,
	"365d": 31536000,
}

var WorkflowCreateCmd = &cobra.Command{
	Use:   "create",
	Short: "Create Workflow",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		teamId, _ := cmd.Flags().GetInt("team-id")
		name, _ := cmd.Flags().GetString("name")
		description, _ := cmd.Flags().GetString("description")
		retention, _ := cmd.Flags().GetString("retention")
		folderId, _ := cmd.Flags().GetString("folder-id")
		tags, _ := cmd.Flags().GetStringSlice("tags")
		disable, _ := cmd.Flags().GetBool("disable")
		priority, _ := cmd.Flags().GetBool("priority")

		if validEventRetention[retention] == 0 {
			fmt.Printf("fatal: retention can have these values: %s", strings.Join(utils.MapKeys(validEventRetention), ", "))
		}

		if err := pkg.CreateWorkflow(teamId, name, description, validEventRetention[retention], folderId, tags, disable, priority); err != nil {
			fmt.Println(err)
			os.Exit(1)
		}

		fmt.Println("Workflow created succesfully")
	},
}

func init() {
	retentionChoices := strings.Join(utils.MapKeys(validEventRetention), "\n\t\t       ")

	WorkflowCreateCmd.Flags().IntP("team-id", "t", 0, "Team ID")
	WorkflowCreateCmd.Flags().StringP("name", "n", "", "Name")
	WorkflowCreateCmd.Flags().StringP("description", "d", "Created with Tines-CLI", "Description")
	WorkflowCreateCmd.Flags().StringP("retention", "r", "1d", fmt.Sprintf("Events retention: %s\n", retentionChoices))
	WorkflowCreateCmd.Flags().StringP("folder-id", "f", "", "Folder ID")
	WorkflowCreateCmd.Flags().StringSlice("tags", []string{}, "Tags")
	WorkflowCreateCmd.Flags().Bool("disable", false, "Disable workflow")
	WorkflowCreateCmd.Flags().Bool("priority", false, "Priority")

	if err := WorkflowCreateCmd.MarkFlagRequired("team-id"); err != nil {
		fmt.Println(err)
	}
}
