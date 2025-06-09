from functions.get_files_info import get_files_info


def run_tests():
    print("Test 1: Current directory (.)")
    print(get_files_info("calculator", "."))
    print()

    print("Test 2: pkg directory")
    print(get_files_info("calculator", "pkg"))
    print()

    print("Test 3: /bin directory (should error)")
    print(get_files_info("calculator", "/bin"))
    print()

    print("Test 4: Parent directory (should error)")
    print(get_files_info("calculator", "../"))


if __name__ == "__main__":
    run_tests()
