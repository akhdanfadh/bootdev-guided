from functions.run_python import run_python_file


def run_tests():
    print("Test 1: Run main.py")
    print(run_python_file("calculator", "main.py"))
    print()

    print("Test 2: Run tests.py")
    print(run_python_file("calculator", "tests.py"))
    print()

    print("Test 3: Run file outside permitted directory")
    print(run_python_file("calculator", "../main.py"))
    print()

    print("Test 4: Run nonexistent file")
    print(run_python_file("calculator", "nonexistent.py"))


if __name__ == "__main__":
    run_tests()
