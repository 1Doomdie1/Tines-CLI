package tenant

import (
	"fmt"
	"os"

	"github.com/1Doomdie1/Tines-CLI/pkg"

	"github.com/spf13/cobra"
)

var AddTennatCmd = &cobra.Command{
	Use:   "add",
	Short: "Add a tenant",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		domain, _ := cmd.Flags().GetString("domain")
		apiKey, _ := cmd.Flags().GetString("api_key")
		checkout, _ := cmd.Flags().GetBool("checkout")
		overwrite, _ := cmd.Flags().GetBool("overwrite")

		if err := pkg.TenantAdd(domain, apiKey, overwrite, checkout); err != nil {
			fmt.Println(err)
			os.Exit(1)
		}
		fmt.Println("Tenant added succesfully")
	},
}

func init() {
	AddTennatCmd.Flags().StringP("domain", "d", "", "Tines domain: https://<DOMAIN>.tines.com")
	AddTennatCmd.Flags().StringP("api_key", "a", "", "API key")
	AddTennatCmd.Flags().BoolP("checkout", "c", false, "Checkout tenant")
	AddTennatCmd.Flags().BoolP("overwrite", "o", false, "Checkout tenant")

	if err := AddTennatCmd.MarkFlagRequired("domain"); err != nil {
		fmt.Println(err)
	}

	if err := AddTennatCmd.MarkFlagRequired("api_key"); err != nil {
		fmt.Println(err)
	}
}
