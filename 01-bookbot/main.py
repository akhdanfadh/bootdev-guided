import sys
from stats import get_num_words, get_num_chars, sort_num_chars

def get_book_text(filepath):
    with open(filepath) as f:
        file_contents = f.read()
    return file_contents

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <path_to_book>")
        sys.exit(1)

    result = get_book_text(sys.argv[1])
    list_chars = sort_num_chars(get_num_chars(result))
    
    print("============ BOOKBOT ============")
    print(f"Analyzing book found at {sys.argv[1]}...")
    print("----------- Word Count ----------")
    print(f"Found {get_num_words(result)} total words")
    print("--------- Character Count -------")
    for item in list_chars:
        if item["char"].isalpha():
            print(f"{item['char']}: {item['num']}")
    print("============= END ===============")

main()
