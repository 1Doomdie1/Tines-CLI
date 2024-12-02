package tenant

import (
	"fmt"
	"os"
	"strconv"

	"github.com/1Doomdie1/Tines-CLI/pkg"

	"github.com/aquasecurity/table"
	"github.com/spf13/cobra"
)

var TenantListCmd = &cobra.Command{
	Use:   "list",
	Short: "List available tenants",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		tenants := pkg.TenantList()
		format, _ := cmd.Flags().GetString("format")

		if len(tenants) == 0 {
			fmt.Println("fatal : No tenants added locally.")
			fmt.Println("run   : tines tenant add -d <DOMAN> -a <API_KEY> --checkout")
			os.Exit(1)
		}

		if format == "text" {
			fmt.Print("\n")
			for _, value := range tenants {
				fmt.Printf("- %s\n", value)
			}

		} else if format == "table" {
			t := table.New(os.Stdout)
			t.SetHeaders("#", "Name")
			t.SetHeaderStyle(table.StyleBold)
			t.SetDividers(table.UnicodeRoundedDividers)

			for index, value := range tenants {
				t.AddRow(strconv.Itoa(index+1), value)
			}

			t.Render()
		} else {
			fmt.Println("fatal: format can have only these values: table & text")
			os.Exit(1)
		}
	},
}

func init() {
	TenantListCmd.Flags().StringP("format", "r", "text", "Output data as text or table")
}
