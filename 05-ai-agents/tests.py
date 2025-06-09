from functions.get_file_content import get_file_content


def run_tests():
    print("Test 1: >10000 chars lorem ipsum")
    print(get_file_content("calculator", "lorem.txt"))
    print()

    print("Test 2: regular file")
    print(get_file_content("calculator", "main.py"))
    print()

    print("Test 3: file in a folder")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    print("Test 4: not in permitted")
    print(get_file_content("calculator", "/bin/cat"))


if __name__ == "__main__":
    run_tests()
