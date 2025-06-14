from functions.run_python import run_python_file

def run_tests():
    print("Test 1: run_python_file('calculator', 'main.py')")
    print(run_python_file("calculator", "main.py"))
    print()

    print("Test 2: run_python_file('calculator', 'tests.py')")
    print(run_python_file("calculator", "tests.py"))
    print()

    print("Test 3: run_python_file('calculator', '../main.py')")
    print(run_python_file("calculator", "../main.py"))
    print()

    print("Test 4: run_python_file('calculator', 'nonexistent.py')")
    print(run_python_file("calculator", "nonexistent.py"))
    print()


if __name__ == "__main__":
    run_tests()
