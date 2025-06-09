from functions.write_file import write_file


def run_tests():
    print("Test 1: regular file")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print()

    print("Test 2: not exist file")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print()

    print("Test 3: not in permitted")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


if __name__ == "__main__":
    run_tests()
