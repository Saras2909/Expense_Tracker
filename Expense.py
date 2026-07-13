import json
import os
import copy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPENSE_FILE = os.path.join(BASE_DIR, "expense.json")
USER_FILE = os.path.join(BASE_DIR, "user_data.json")

default_expense_list = {
  "Categories": {
    "Groceries": {},
    "Dining Out": {},
    "Rent / Mortgage": {},
    "Utilities": {},
    "Transport": {},
    "Insurance": {},
    "Health & Medical": {},
    "Personal Care": {},
    "Entertainment": {},
    "Subscriptions": {},
    "Shopping": {},
    "Clothing": {},
    "Education": {},
    "Gifts & Donations": {},
    "Travel": {},
    "Accommodation": {},
    "Vehicle Maintenance": {},
    "Taxes": {},
    "Pet Care": {},
    "Home Improvement": {},
    "Childcare": {},
    "Miscellaneous": {},
    "Investment":{}
  }
}
def load_data():
    global expense_dict, user_data
    try:
        with open(EXPENSE_FILE, "r") as f:
            expense_dict = json.load(f)
    except FileNotFoundError:
        expense_dict = {}
        print("Expense data file not found. Starting with a new expense list.")
    except json.JSONDecodeError:
        expense_dict = {}
        print("Expense data file is invalid. Starting with a new expense list.")

    try:
        with open(USER_FILE, "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        user_data = {}
        print("User data file not found. Starting with a new user list.")
    except json.JSONDecodeError:
        user_data = {}
        print("User data file is invalid. Starting with a new user list.")


load_data()

def save():
    try:
        #First we make a temp file and then write it as if the temp file gets
        #corrupted it wont disturb the main file
        tmp_path = EXPENSE_FILE + ".tmp"
        with open(tmp_path, "w") as f:
            json.dump(expense_dict, f, indent=2)
        os.replace(tmp_path, EXPENSE_FILE)  
    except (OSError, TypeError, ValueError) as e:
        print(f"Unable to save expenses: {e}")


#Expense class have all methods related to expense of the user
class Expense:
    def __init__(self,user,cat):
        self.main(user,cat)
    def add_expense(self,user,cat):
        try:
            expense_with_amount = input('Enter expense name and amount :-').split()
            expense_dict[user]["Categories"][cat][expense_with_amount[0]] = float(expense_with_amount[1])
            save()
        except ValueError:
            print("Amount must be an integer value only.")

    def view_expense(self,user,cat):
        if cat not in expense_dict[user]["Categories"].keys():
            print("Category not found.")
            return
        items = expense_dict[user]["Categories"][cat]
        if not items:
            print("No expenses in this category.")
            return
        for key, value in items.items():
            print(f"{key} : {value}")

    def modify_expense(self,user,cat):
        print("Enter the name of expense you want to modify from the given list of expense:-")
        self.view_expense(user,cat)
        if not expense_dict[user]["Categories"][cat]:
            print("Your expense log is empty.")
        else:
            expense_modify = input()
            if expense_modify in expense_dict[user]["Categories"][cat]:
                current_amount = expense_dict[user]["Categories"][cat][expense_modify]
                print(f"Current amount for '{expense_modify}': {current_amount}")
                print("Choose modification:")
                print("1) Add money to this expense")
                print("2) Subtract money from this expense")
                print("3) Rename expense")
                print("4) Set a new amount")
                print("5) Cancel")
                action = input("Enter option: ")
                if action == "1":
                    try:
                        amt_chn = float(input("Enter amount to add: "))
                        expense_dict[user]["Categories"][cat][expense_modify] = current_amount + amt_chn
                        save()
                        print("Amount updated.")
                    except ValueError:
                        print("Enter a valid number.")
                elif action == "2":
                    try:
                        amt_chn = float(input("Enter amount to subtract: "))
                        expense_dict[user]["Categories"][cat][expense_modify] = current_amount - amt_chn
                        save()
                        print("Amount updated.")
                    except ValueError:
                        print("Enter a valid number.")
                elif action == "3":
                    new_name = input("Enter new expense name: ").strip()
                    if not new_name:
                        print("Name cannot be empty.")
                    elif new_name in expense_dict[user]["Categories"][cat]:
                        print("An expense with that name already exists.")
                    else:
                        expense_dict[user]["Categories"][cat][new_name] = expense_dict[user]["Categories"][cat].pop(expense_modify)
                        save()
                        print("Expense renamed.")
                elif action == "4":
                    try:
                        new_amount = float(input("Enter new amount: "))
                        expense_dict[user]["Categories"][cat][expense_modify] = new_amount
                        save()
                        print("Amount changed.")
                    except ValueError:
                        print("Enter a valid number.")
                elif action == "5":
                    print("No changes made.")
                else:
                    print("Invalid option")
            else:
                print('Expense not found.')

    #It displays the total amount spend by the user in a specific category
    def total_expense(self,user,cat):
        print(f"Total expense is :- {sum(expense_dict[user]['Categories'][cat].values())}")

    def main(self,user,cat):
        flag = True
        while(flag):

            print("""Please select an task from below:-
            Enter 1 to Add an expense
            Enter 2 to View all expenses
            Enter 3 to Modify an expense
            Enter 4 to Show total expenses
            Enter 5 to Exit program""")
            try:
                task = int(input("Enter the task number you want to perform :- "))
            except ValueError:
                print("Enter a valid integer")
                continue
            if(task == 1):
                self.add_expense(user,cat)
            elif(task == 2):
                print("Your expenses are listed below:- ")
                self.view_expense(user,cat)
            elif(task == 3):
                self.modify_expense(user,cat)
            elif(task == 4):
                self.total_expense(user,cat)
            elif(task == 5):
                print('Exiting the program....')
                flag = False
            else:
                print("Invalid input")

#Categories Class
class Categories:
    #To display the list of categories the user have
    @staticmethod
    def display(user):
        categories = sorted(expense_dict[user]["Categories"].keys())
        for i in categories:
            print(i)

    #To display the main expense menu
    @staticmethod
    def menu(user):
        while True:
            categories = list(expense_dict[user]["Categories"].keys())
            print("\nWelcome to Expense Tracker :- ")
            print("Enter 1 to choose a category")
            print("Enter 2 to add a category")
            print("Enter 3 to exit")
            choice = input("Your choice: ")
            if choice == "1":
                if not categories:
                    print("No categories available. Add one first.")
                    continue
                print("Choose a category from given below list:- ")
                Categories.display(user)
                category = input().strip()
                if not category:
                    print("Category name cannot be empty.")
                    continue
                if category in expense_dict[user]["Categories"]:
                    Expense(user,category)
                else:
                    print("Category name not there in the category list.\nPlease add the category first and then continue")
                    continue
            elif choice == "2":
                new_cat = input("Enter new category name: ")
                if not new_cat:
                    print("Category name cannot be empty.")
                    continue
                if new_cat in expense_dict[user]["Categories"]:
                    print("Category already exists.")
                    continue
                expense_dict[user]["Categories"][new_cat] = {}
                save()
                print(f"Category '{new_cat}' added.")
            elif choice == "3":
                save()
                print("Exiting...")
                break
            else:
                print("Invalid option")
                continue

def login():
    try:
        name = input("Enter your name to login :- ")
        password = input("Enter your password to login :- ")
        if not name or not password:
            raise ValueError("Name and password cannot be empty.")
        if name not in user_data:
            raise KeyError("User not found. Please register first.")
        if password == user_data[name]:
            print("Login successful.")
            Categories.menu(name)
            return True
        raise ValueError("Incorrect password.")
    except KeyError as e:
        print(e)
        return False
    except ValueError as e:
        print(e)
        return False


def register():
    global user_data
    try:
        name = input("Enter your name to register :- ").strip()
        password = input("Set a password :- ").strip()
        if not name or not password:
            raise ValueError("Name and password cannot be empty.")
        if name in user_data:
            raise KeyError("User already exists. Please login instead.")

        while True:
            re_pass = input("Enter your password again :- ").strip()
            if password != re_pass:
                print("Your re-entered password doesn't match.")
                continue
            user_data[name] = password
            with open(USER_FILE, "w") as f:
                json.dump(user_data, f, indent=2)
            expense_dict[name] = copy.deepcopy(default_expense_list)
            with open(EXPENSE_FILE,"w") as f:
                json.dump(expense_dict,f,indent=2)
            print("Registered Successfully")
            break
    except KeyError as e:
        print(e)
    except ValueError as e:
        print(e)
    except OSError as e:
        print(f"Unable to save user data: {e}")


def start_cli():
    while True:
        print("\nWelcome to Expense Tracker")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        try:
            choice = int(input("Enter your choice: ").strip())
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            register()
        elif choice == 2:
            if login():
                break
        elif choice == 3:
            print("Exiting....")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    start_cli()
