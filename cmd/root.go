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
	Short: "Tines multi-tenant management tool",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		version, _ := cmd.Flags().GetBool("version")
		if version {
			fmt.Println("v4.3.0")
			os.Exit(0)
		}
		if len(args) == 0 {
			cmd.Help()
		}
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

	rootCmd.SetHelpCommand(&cobra.Command{Hidden: true})
	rootCmd.CompletionOptions.DisableDefaultCmd = true

	rootCmd.Flags().BoolP("version", "v", false, "Show CLI version")
}
