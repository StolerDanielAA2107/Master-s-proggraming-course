import os
from company import Company


def main():
    company = Company()
    actions = {
        1: company.add_employee,
        2: company.edit_employee,
        3: company.delete_employee,
        4: company.print_list,
        5: company.save_to_file,
        6: company.load_from_file,
        7: company.clear_list
    }

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  
        print("\nMenu:")
        print("1 - Add object")
        print("2 - Edit object")
        print("3 - Delete object")
        print("4 - Print list")
        print("5 - Save to file")
        print("6 - Load from file")
        print("7 - Clear list")
        print("0 - Exit")
        try:
            choice = int(input("Enter choice: "))
            if choice == 0:
                break
            elif choice in actions:
                actions[choice]()
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input. Enter a number.")
        input("Press Enter to continue...") 

if __name__ == "__main__":
    main()