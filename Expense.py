import json

with open("data.json","r") as f:
    expense_dict  = json.load(f)

class Expense:
    def __init__(self,cat):
        self.main(cat)

    def add_expense(self,cat):
        try:
            expense_with_amount = input('Enter expense name and amount :-').split()
            expense_dict["Categories"][cat][expense_with_amount[0]] = float(expense_with_amount[1])
            save()
        except ValueError:
            print("Amount must be an integer value only.")

    def view_expense(self,cat):
        if cat not in expense_dict.get("Categories", {}):
            print("Category not found.")
            return
        items = expense_dict["Categories"][cat]
        if not items:
            print("No expenses in this category.")
            return
        for key, value in items.items():
            print(f"{key} : {value}")

    def modify_expense(self,cat):
        print("Enter the name of expense you want to modify from the given list of expense:-")
        self.view_expense(cat)
        if not expense_dict["Categories"][cat]:
            print("Your expense log is empty.")
        else:
            expense_modify = input().strip()
            if expense_modify in expense_dict["Categories"][cat]:
                current_amount = expense_dict["Categories"][cat][expense_modify]
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
                        expense_dict["Categories"][cat][expense_modify] = current_amount + amt_chn
                        save()
                        print("Amount updated.")
                    except ValueError:
                        print("Enter a valid number.")
                elif action == "2":
                    try:
                        amt_chn = float(input("Enter amount to subtract: "))
                        expense_dict["Categories"][cat][expense_modify] = current_amount - amt_chn
                        save()
                        print("Amount updated.")
                    except ValueError:
                        print("Enter a valid number.")
                elif action == "3":
                    new_name = input("Enter new expense name: ").strip()
                    if not new_name:
                        print("Name cannot be empty.")
                    elif new_name in expense_dict["Categories"][cat]:
                        print("An expense with that name already exists.")
                    else:
                        expense_dict["Categories"][cat][new_name] = expense_dict["Categories"][cat].pop(expense_modify)
                        save()
                        print("Expense renamed.")
                elif action == "4":
                    try:
                        new_amount = float(input("Enter new amount: "))
                        expense_dict["Categories"][cat][expense_modify] = new_amount
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

    def total_expense(self,cat):
        print(f"Total expense is :- {sum(expense_dict["Categories"][cat].values())}")

    def main(self,cat):
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
                self.add_expense(cat)
            elif(task == 2):
                print("Your expenses are listed below:- ")
                self.view_expense(cat)
            elif(task == 3):
                self.modify_expense(cat)
            elif(task == 4):
                self.total_expense(cat)
            elif(task == 5):
                print('Exiting the program....')
                flag = False
            else:
                print("Invalid input")

def display():
    categories = sorted(expense_dict.get("Categories", {}).keys())
    for i in categories:
        print(i)

def save():
        with open("data.json", "w") as f:
            json.dump(expense_dict, f, indent=2)
flag = True
while True:
    categories = list(expense_dict["Categories"].keys())
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
        display()
        category = input()
        if not category:
            print("Category name cannot be empty.")
            continue
        if category in expense_dict["Categories"]:
            E = Expense(category)
        else:
            print("""Category name not there in the category list.\n
                  Please add the category first and then continue""")
            continue
    elif choice == "2":
        new_cat = input("Enter new category name: ").strip()
        if not new_cat:
            print("Category name cannot be empty.")
            continue
        if new_cat in expense_dict["Categories"]:
            print("Category already exists.")
            continue
        expense_dict["Categories"][new_cat] = {}
        save()
        print(f"Category '{new_cat}' added.")
    elif choice == "3":
        save()
        print("Exiting...")
        break
    else:
        print("Invalid option")
        continue