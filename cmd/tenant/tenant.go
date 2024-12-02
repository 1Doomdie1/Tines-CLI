package tenant

import (
	"github.com/spf13/cobra"
)

var TenantCmd = &cobra.Command{
	Use:   "tenant",
	Short: "Manage tenants",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		cmd.Help()
	},
}

func init() {
	TenantCmd.AddCommand(AddTennatCmd)
	TenantCmd.AddCommand(TenantInfoCmd)
	TenantCmd.AddCommand(TenantListCmd)
	TenantCmd.AddCommand(CheckoutCmd)
	TenantCmd.SetHelpCommand(&cobra.Command{Hidden: true})
}
