package cmd

import (
	"fmt"
	"os"

	"github.com/1Doomdie1/Tines-CLI/cmd/team"
	"github.com/1Doomdie1/Tines-CLI/cmd/tenant"
	"github.com/1Doomdie1/Tines-CLI/cmd/workflow"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "tines",
	Short: "TInes multi tenant management tool",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("v0.1.0")
	},
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	rootCmd.AddCommand(team.TeamCmd)
	rootCmd.AddCommand(tenant.TenantCmd)
	rootCmd.AddCommand(workflow.WorkflowCmd)

	// Disable default help cmd and completion
	rootCmd.SetHelpCommand(&cobra.Command{Hidden: true})
	rootCmd.CompletionOptions.DisableDefaultCmd = true
}
