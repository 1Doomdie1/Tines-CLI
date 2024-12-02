package tenant

import (
	"fmt"
	"os"

	"github.com/1Doomdie1/Tines-CLI/pkg"

	"github.com/spf13/cobra"
)

var CheckoutCmd = &cobra.Command{
	Use:   "checkout",
	Short: "Checkout tenant",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {

		domain, _ := cmd.Flags().GetString("domain")

		if domain == "" {
			cmd.Help()
			os.Exit(1)
		}

		if err := pkg.TenantCheckout(domain); err != nil {
			fmt.Println("fatal: unknown tenant")
			fmt.Println("Recomanded commands")
			fmt.Println("   -> tines tenant list                                      |   list local tennats")
			fmt.Println("   -> tines tenant checkout -d <DOMAIN>                      |   checkout tenant")
			fmt.Println("   -> tines tenant add -d <DOMAIN> -a <API_KEY> --checkout   |   add new tenant")
			os.Exit(1)
		}
	},
}

func init() {
	CheckoutCmd.Flags().StringP("domain", "d", "", "Domain name")
}
