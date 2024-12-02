package workflow

import (
	"fmt"
	"os"

	"github.com/1Doomdie1/Tines-CLI/pkg"
	"github.com/spf13/cobra"
)

var WorkflowCmd = &cobra.Command{
	Use:   "workflow",
	Short: "Manage workflows",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		if !pkg.IsTenantSet() {
			fmt.Println("fatal: No tenant set.")
			fmt.Println("Recomanded commands")
			fmt.Println("   -> tines tenant checkout -d <DOMAIN> | checkout tenant")
			os.Exit(1)
		}
		cmd.Help()
	},
}

func init() {
	WorkflowCmd.AddCommand(WorkflowCreateCmd)
	WorkflowCmd.AddCommand(WorkflowListCmd)
}
