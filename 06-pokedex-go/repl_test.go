package main

import (
	"fmt"
	"testing"
)

func TestCleanInput(test *testing.T) {
	testCases := []struct {
		input    string
		expected []string
	}{
		{
			// case 1: white spaces
			input:    "  \thello world  hello\tworld\nhello \nworld\n",
			expected: []string{"hello", "world", "hello", "world", "hello", "world"},
		},
		{
			// case 2: lowercase
			input:    "HELLO wOrLd hello 世界",
			expected: []string{"hello", "world", "hello", "世界"},
		},
	}

	// loop over cases and run tests
	for _, testCase := range testCases {
		actual := cleanInput(testCase.input)
		fail_log := fmt.Sprintf(
			"cleanInput(\"%v\") = %v; want %v",
			testCase.input, actual, testCase.expected)

		// check length
		if len(actual) != len(testCase.expected) {
			test.Error(fail_log)
		}

		// check content
		for i := range actual {
			word := actual[i]
			expectedWord := testCase.expected[i]
			if word != expectedWord {
				test.Error(fail_log)
				break
			}
		}
	}
}
