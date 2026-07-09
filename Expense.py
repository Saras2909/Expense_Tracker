flag = True
expense_dict = {}
def add_expense():
    try:
        expense_with_amount = input('Enter expense name and amount :-').split()
        expense_dict[expense_with_amount[0]] = int(expense_with_amount[1])
    except ValueError:
        print("Amount must be an integer value only.")

def view_expense():
    for key,value in expense_dict.items():
        print(f"{key} : {value}")

def delete_expense():
    print("Enter the name of expense you want to delete from the given list of expense:-")
    view_expense()
    if not expense_dict:
        print("Your expense log is empty.")
    else:
        expense_delete = input()
        if(expense_delete in expense_dict):
            del expense_dict[expense_delete]
        else:
            print('Expense not found.')

def total_expense():
    print(f"Total expense is :- {sum(expense_dict.values())}")

while(flag):

    print("""Welcome to expense tracker. Please select an task from below:-
      Enter 1 to Add an expense
      Enter 2 to View all expenses
      Enter 3 to Delete an expense
      Enter 4 to Show total expenses
      Enter 5 to Exit program""")
    try:
        task = int(input("Enter the task number you want to perform :- "))
    except ValueError:
        print("Enter a valid integer")
        continue
    if(task == 1):
        add_expense()
    elif(task == 2):
        print("Your expenses are listed below:- ")
        view_expense()
    elif(task == 3):
        delete_expense()
    elif(task == 4):
        total_expense()
    elif(task == 5):
        print('Exiting the program....')
        flag = False
    else:
        print("Invalid input")
