package pkg

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/1Doomdie1/Tines-CLI/pkg/httpClient"
)

type Workflow struct {
	Name                                    string      `json:"name"`
	UserID                                  int         `json:"user_id"`
	Description                             string      `json:"description"`
	KeepEventsFor                           int         `json:"keep_events_for"`
	Disabled                                bool        `json:"disabled"`
	Priority                                bool        `json:"priority"`
	SendToStoryEnabled                      bool        `json:"send_to_story_enabled"`
	SendToStoryAccessSource                 string      `json:"send_to_story_access_source"`
	SendToStoryAccess                       string      `json:"send_to_story_access"`
	SendToStorySkillUseRequiresConfirmation bool        `json:"send_to_story_skill_use_requires_confirmation"`
	SharedTeamSlugs                         []string    `json:"shared_team_slugs"`
	EntryAgentid                            int         `json:"entry_agent_id"`
	ExitAgents                              interface{} `json:"exit_agents"`
	TeamID                                  int         `json:"team_id"`
	Tags                                    []string    `json:"tags"`
	GUID                                    string      `json:"guid"`
	Slug                                    string      `json:"slug"`
	CreatedAt                               string      `json:"created_at"`
	UpdatedAt                               string      `json:"updated_at"`
	EditedAt                                string      `json:"edited_at"`
	Mode                                    string      `json:"mode"`
	ID                                      int         `json:"id"`
	FolderID                                int         `json:"folder_id"`
	Published                               bool        `json:"published"`
	ChangeControlEnabled                    bool        `json:"change_control_enabled"`
	Locked                                  bool        `json:"locked"`
	Owners                                  []int       `json:"owners"`
}

func CreateWorkflow(teamId int, name string, description string, eventRetention int, folderId string, tags []string, disabled bool, priority bool) error {
	data := map[string]interface{}{
		"team_id":         teamId,
		"name":            name,
		"description":     description,
		"keep_events_for": eventRetention,
		"folder_id":       folderId,
		"tags":            tags,
		"disabled":        disabled,
		"priority":        priority,
	}

	resp, statusCode, err := httpClient.CallEndpoint("POST", "/stories", nil, data)

	if err != nil {
		return err
	}

	if statusCode != http.StatusCreated {
		return fmt.Errorf("fatal: %v", string(resp))
	}

	return nil
}

func ListWorkflows(teamId string, folderId string, tags []string, filter string, order string) ([]Workflow, error) {
	data := map[string]interface{}{
		"team_id":   teamId,
		"folder_id": folderId,
		"tags":      tags,
		"filter":    filter,
		"order":     order,
		"per_page":  500,
	}

	resp, _, err := httpClient.CallEndpoint("GET", "/stories", nil, data)

	if err != nil {
		return nil, err
	}

	var responseData struct {
		Workflows []Workflow `json:"stories"`
	}

	err = json.Unmarshal(resp, &responseData)
	if err != nil {
		return nil, err
	}

	return responseData.Workflows, nil

}
