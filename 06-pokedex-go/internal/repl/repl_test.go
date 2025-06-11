package repl

import (
	"reflect"
	"testing"
)

func TestCleanInput(t *testing.T) {
	tests := []struct {
		name string
		input    string
		want []string
	}{
		{
			name:  "handles multiple whitespace types",
			input: "  \thello world  hello\tworld\nhello \nworld\n",
			want:  []string{"hello", "world", "hello", "world", "hello", "world"},
		},
		{
			name:  "converts to lowercase",
			input: "HELLO wOrLd hello 世界",
			want:  []string{"hello", "world", "hello", "世界"},
		},
		{
			name:  "empty input",
			input: "",
			want:  []string{},
		},
		{
			name:  "only whitespace",
			input: "   \t\n   ",
			want:  []string{},
		},
		{
			name:  "single word",
			input: "pokemon",
			want:  []string{"pokemon"},
		},
		{
			name:  "preserves unicode characters",
			input: "Pikachu ピカチュウ 皮卡丘",
			want:  []string{"pikachu", "ピカチュウ", "皮卡丘"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := cleanInput(tt.input)
			if !reflect.DeepEqual(got, tt.want) {
				t.Errorf("cleanInput(%q) = %v, want %v", tt.input, got, tt.want)
			}
		})
	}
}
