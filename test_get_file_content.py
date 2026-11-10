from functions.get_file_content import get_file_content

def main():
    # Test 1
    test1 = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(test1)}")
    print(f"lorem.txt truncated: {'truncated' in test1}")
    
    # Test 2
    test2 = get_file_content("calculator", "main.py")
    print(test2)

    # Test 3
    test3 = get_file_content("calculator", "pkg/calculator.py")
    print(test3)

    # Test 4
    test4 = get_file_content("calculator", "/bin/cat")
    print(test4)

    # Test 5
    test5 = get_file_content("calculator", "pkg/does_not_exist.py")
    print(test5)

main()
