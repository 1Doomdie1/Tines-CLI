package pkg

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"os"
	"strings"

	"github.com/1Doomdie1/Tines-CLI/pkg/httpClient"

	"github.com/joho/godotenv"
)

type Tenant struct {
	Domain string
	ApiKey string
}

type TenantData struct {
	Stack struct {
		EgressIPs []string `json:"egress_ips"`
		Name      string   `json:"name"`
		Region    string   `json:"region"`
		Type      string   `json:"type"`
	} `json:"stack"`
}

func TenantAdd(domain string, apiKey string, overwrite bool, checkout bool) error {
	tenant := Tenant{
		Domain: domain,
		ApiKey: apiKey,
	}

	tenantPath := fmt.Sprintf("tenants/%s.json", domain)
	if _, err := os.Stat(tenantPath); errors.Is(err, os.ErrNotExist) || overwrite {

		if !tenant.CheckCreds() {
			return errors.New("fatal: invalid credentials")
		}

		file, _ := os.Create(tenantPath)
		defer file.Close()

		encoder := json.NewEncoder(file)
		encoder.SetIndent("", "\t")

		if err = encoder.Encode(tenant); err != nil {
			return err
		}

		if checkout {
			TenantCheckout(domain)
		}

		return nil
	}
	return errors.New("tenant already exists")
}

func TenantInfo() (TenantData, error) {
	resp, statusCode, err := httpClient.CallEndpoint("GET", "/info", nil, nil)

	if statusCode != http.StatusOK {
		return TenantData{}, fmt.Errorf("%s", string(resp))
	}

	if err != nil {
		return TenantData{}, err
	}

	var tenantData TenantData
	err = json.Unmarshal(resp, &tenantData)

	if err != nil {
		return TenantData{}, err
	}

	return tenantData, nil
}

func TenantCheckout(domain string) error {
	tenantPath := fmt.Sprintf("tenants/%s.json", domain)

	if _, err := os.Stat(tenantPath); errors.Is(err, os.ErrNotExist) {
		return err
	}

	envVars := map[string]string{
		"USE_TENANT": domain,
	}

	godotenv.Write(envVars, ".env")
	fmt.Printf("Now using %s tenant\n", domain)
	return nil
}

func (t *Tenant) CheckCreds() bool {
	url := "https://" + t.Domain + ".tines.com/api/v1/info"
	client := http.Client{}

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return false
	}

	req.Header.Add("Authorization", "Bearer "+t.ApiKey)

	resp, err := client.Do(req)
	if err != nil {
		return false
	}
	defer resp.Body.Close()

	return resp.StatusCode == http.StatusOK

}

func TenantList() []string {
	entries, _ := os.ReadDir("tenants")

	tenants := make([]string, len(entries))

	for i, e := range entries {
		tenants[i] = strings.Replace(e.Name(), ".json", "", -1)
	}

	return tenants
}

func IsTenantSet() bool {
	godotenv.Load(".env")

	tenant := os.Getenv("USE_TENANT")

	if tenant == "" || tenant == "None" {
		return false
	}
	return true
}
