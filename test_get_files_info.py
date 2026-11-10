from functions.get_files_info import get_files_info 
def main():
    # Test 1
    test1 = get_files_info("calculator", ".")
    print("Result for current directory:") 
    print(f"  {test1}")

    # Test 2
    test2 = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory")
    print(f"  {test2}")

    # Test 3
    test3 = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory")
    print(f"  {test3}")

    # Test 4
    test4 = get_files_info("calculator", "../")
    print("Result for '../' directory")
    print(f"  {test4}")

main()
