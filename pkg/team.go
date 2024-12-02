package pkg

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/1Doomdie1/Tines-CLI/pkg/httpClient"
)

type Team struct {
	Teams []struct {
		ID     int
		Name   string
		Groups []struct {
			ID   int
			Name string
		} `json:"groups"`
	} `json:"teams"`
}

type TeamMembers struct {
	Members []struct {
		ID                 int    `json:"id"`
		FirstName          string `json:"first_name"`
		LastName           string `json:"last_name"`
		Email              string `json:"email"`
		IsAdmin            bool   `json:"is_admin"`
		CreatedAt          string `json:"created_at"`
		LastSeen           string `json:"last_seen"`
		InvitationAccepted bool   `json:"invitation_accepted"`
		Role               string `json:"role"`
	} `json:"members"`
}

func TeamList() (Team, error) {
	resp, _, err := httpClient.CallEndpoint("GET", "/teams", nil, nil)

	if err != nil {
		return Team{}, err
	}

	var team Team
	err = json.Unmarshal(resp, &team)

	if err != nil {
		return Team{}, err
	}

	return team, nil
}

func TeamCreate(name string) error {
	data := map[string]interface{}{
		"name": name,
	}

	resp, statusCode, err := httpClient.CallEndpoint("POST", "/teams", nil, data)

	if err != nil {
		return err
	}

	if statusCode != http.StatusOK {
		return fmt.Errorf("%s", string(resp))
	}

	return nil
}

func UpdateTeam(name string, teamId int) error {
	data := map[string]interface{}{
		"name": name,
	}

	resp, statusCode, err := httpClient.CallEndpoint("PUT", fmt.Sprintf("/teams/%v", teamId), nil, data)

	if err != nil {
		return err
	}

	if statusCode != http.StatusOK {
		return fmt.Errorf("%s", string(resp))
	}

	return nil
}

func GetTeamMembers(teamId int) (TeamMembers, error) {
	data := map[string]interface{}{
		"per_page": 500,
	}

	resp, statusCode, err := httpClient.CallEndpoint("GET", fmt.Sprintf("/teams/%v/members", teamId), nil, data)

	if err != nil {
		return TeamMembers{}, err
	}

	if statusCode != http.StatusOK {
		return TeamMembers{}, fmt.Errorf("%s", string(resp))
	}

	var teamMembers TeamMembers
	err = json.Unmarshal(resp, &teamMembers)

	if err != nil {
		return TeamMembers{}, err
	}

	return teamMembers, nil
}

func RemoveTeamMember(teamId int, userId int) error {
	data := map[string]interface{}{
		"user_id": userId,
	}

	resp, statusCode, err := httpClient.CallEndpoint("POST", fmt.Sprintf("/teams/%v/remove_member", teamId), nil, data)

	if err != nil {
		return err
	}

	if statusCode != http.StatusOK {
		return fmt.Errorf("%s", string(resp))
	}

	return nil
}

func InviteTeamMember(teamId int, email string, role string) error {
	data := map[string]interface{}{
		"email": email,
		"role":  role,
	}

	resp, statusCode, err := httpClient.CallEndpoint("POST", fmt.Sprintf("/teams/%v/invite_member", teamId), nil, data)

	if err != nil {
		return err
	}

	if statusCode != http.StatusOK {
		return fmt.Errorf("%s", string(resp))
	}

	return nil
}
