from functions.run_python_file import run_python_file

def main():
    # Test 1
    test1 = run_python_file("calculator", "main.py")
    print(test1)

    # Test 2
    test2 = run_python_file("calculator", "main.py", ["3 + 5"])
    print(test2)

    # Test 3
    test3 = run_python_file("calculator", "tests.py")
    print(test3)

    # Test 4
    test4 = run_python_file("calculator", "../main.py")
    print(test4)

    # Test 5
    test5 = run_python_file("calculator", "nonexistent.py")
    print(test5)

    # Test 6
    test6 = run_python_file("calculator", "lorem.txt")
    print(test6)

main()
