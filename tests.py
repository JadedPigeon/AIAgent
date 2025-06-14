from functions.get_file_content import get_file_content

def run_tests():
    print("Test 1: get_file_content('calculator', 'main.py')")
    print(get_file_content("calculator", "main.py"))
    print()

    print("Test 2: get_file_content('calculator', 'pkg/calculator.py')")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    print("Test 3: get_file_content('calculator', '/bin/cat')")
    print(get_file_content("calculator", "/bin/cat"))
    print()

if __name__ == "__main__":
    run_tests()
