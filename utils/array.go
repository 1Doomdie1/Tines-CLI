package utils

func IsStringInArray(str string, array []string) bool {
	for _, value := range array {
		if value == str {
			return true
		}
	}
	return false
}
