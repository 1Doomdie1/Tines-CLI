package httpClient

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"

	"github.com/joho/godotenv"
)

func CallEndpoint(method string, endpoint string, headers map[string]string, body map[string]interface{}) ([]byte, int, error) {
	dtnv, _ := godotenv.Read(".env")

	if dtnv["USE_TENANT"] == "None" {
		fmt.Println("fatal: No tenant set.")
		fmt.Println("Recomanded commands")
		fmt.Println("   -> tines tenant checkout -d <DOMAIN> | checkout tenant")
		os.Exit(1)
	}

	content, err := os.ReadFile(fmt.Sprintf("tenants/%s.json", dtnv["USE_TENANT"]))

	if err != nil {
		log.Fatal(err)
	}

	var tenantData map[string]string

	err = json.Unmarshal(content, &tenantData)
	if err != nil {
		log.Fatal(err)
	}

	baseURL := fmt.Sprintf("https://%s.tines.com/api/v1", tenantData["Domain"])
	fullURL := fmt.Sprintf("%s%s", baseURL, endpoint)

	defaultHeaders := map[string]string{
		"Authorization": fmt.Sprintf("Bearer %s", tenantData["ApiKey"]),
		"Content-Type":  "application/json",
	}

	for key, value := range headers {
		defaultHeaders[key] = value
	}

	var requestBody io.Reader
	if body != nil {
		bodyBytes, err := json.Marshal(body)
		if err != nil {
			return nil, 0, fmt.Errorf("failed to marshal body: %w", err)
		}
		requestBody = bytes.NewReader(bodyBytes)
	}

	req, err := http.NewRequest(method, fullURL, requestBody)
	if err != nil {
		return nil, 0, fmt.Errorf("failed to create request: %w", err)
	}

	for key, value := range defaultHeaders {
		req.Header.Add(key, value)
	}

	client := &http.Client{}
	response, err := client.Do(req)
	if err != nil {
		return nil, 0, fmt.Errorf("request failed: %w", err)
	}
	defer response.Body.Close()

	respBody, err := io.ReadAll(response.Body)
	if err != nil {
		return nil, 0, fmt.Errorf("failed to read response body: %w", err)
	}

	return respBody, response.StatusCode, nil
}
