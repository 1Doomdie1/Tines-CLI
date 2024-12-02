package tenant

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"

	"github.com/1Doomdie1/Tines-CLI/pkg"

	"github.com/aquasecurity/table"
	"github.com/spf13/cobra"
)

var TenantInfoCmd = &cobra.Command{
	Use:   "info",
	Short: "Get basic tenant information",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		format, _ := cmd.Flags().GetString("format")

		if !pkg.IsTenantSet() {
			fmt.Println("fatal : No tenant set.")
			fmt.Println("run   : tines tenant checkout -d <tenant>")
			os.Exit(1)
		}

		tenantInfo, err := pkg.TenantInfo()

		if err != nil {
			fmt.Printf("%v", err)
			os.Exit(1)
		}

		if format == "text" {
			msg := fmt.Sprintf(
				"\n"+
					"###############################\n"+
					"#            Stack            #\n"+
					"###############################\n"+
					"- Name        :  %s\n"+
					"- Region      :  %s\n"+
					"- Type        :  %s\n"+
					"- Egress IPs  :  %s",
				tenantInfo.Stack.Name,
				tenantInfo.Stack.Region,
				tenantInfo.Stack.Type,
				strings.Join(tenantInfo.Stack.EgressIPs, "\n\t\t "),
			)

			fmt.Println(msg)
		} else if format == "table" {
			t := table.New(os.Stdout)
			t.SetHeaders("Attribute", "Value")
			t.SetHeaderStyle(table.StyleBold)
			t.SetDividers(table.UnicodeRoundedDividers)

			t.AddRow("Name", tenantInfo.Stack.Name)
			t.AddRow("Region", tenantInfo.Stack.Region)
			t.AddRow("Type", tenantInfo.Stack.Type)
			t.AddRow("IPS", strings.Join(tenantInfo.Stack.EgressIPs, "\n"))

			t.Render()
		} else if format == "json" {
			jsonOutput, err := json.MarshalIndent(tenantInfo, "", "  ")
			if err != nil {
				fmt.Printf("error: could not marshal tenant info to JSON: %v", err)
				os.Exit(1)
			}
			fmt.Println(string(jsonOutput))
		} else {
			fmt.Println("fatal: format can have only these values: table, json & text")
			os.Exit(1)
		}
	},
}

func init() {
	TenantInfoCmd.Flags().StringP("format", "r", "text", "Output data as json, table or text")
}
