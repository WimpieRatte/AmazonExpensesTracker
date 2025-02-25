import re
import time
import datetime

user = ""
password = ""
phone_number = ""
purchases = {}


def login_registration():
    """
    Processes the registration of a new login
    """
    print("\n####################### Login Registration:")
    print("Please enter a username and password for registration.")
    print("Password rules:")
    print("""
        Should have at least one number.
        Should have at least one uppercase and one lowercase character.
        Should have at least one special symbol.
        Should be between 6 to 20 characters long.
        If the password is not valid the user will be ask to try again with a valid password, then exit the program.
        """)
    global user
    user = input("Username: ")
    global password
    password = input("Password: ")
    while not validate_password_complexity(password):
        password = input("Password is not complex enough. Please try again: ")
    
def validate_password_complexity(password):
    """
    Validates the complexity of the given password

    Args:
        password (_type_): The password to validate

    Returns:
        _type_: bool: Whether its complex enough or not.
    """
    # Should have at least one number, upper and lower case letters, special symbol and 6-20 characters long
    if re.match(pattern=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^0-9a-zA-Z]).{6,20}$",string=password):
        return True
    else:
        return False

def input_Germany_number():
    """
    Prompts for a Germany number until a corretly formatted one is typed.
    """
    print("\n####################### Phone number registration:")
    formatted_wrong = True
    global phone_number
    while formatted_wrong:
        phone_number = input("Please enter a valid Germany phone number:")
        if re.match(pattern=r"(\(?([\d \-\)\–\+\/\(]+){6,}\)?([ .\-–\/]?)([\d]+))", string=phone_number):
            formatted_wrong = False
            
def login():
    """
    Prompts user for login and handles it when entered incorrectly multiple times.

    Returns:
        _type_: If 0, login successful. If -1, login unsuccessful.
    """
    print("\n####################### Login:")
    fail_counter = 0
    while True:
        user_attempt = input("Username: ")
        pass_attempt = input("Password: ")
        if user_attempt == user and pass_attempt == password:
            print("Welcome to the Amazon Expense Tracker!")
            return 0 # login success
        elif fail_counter == 2:
            print("You have used up all your attempts. Please try again after waiting 5 seconds")
            time.sleep(5)  # wait 5 seconds
            fail_counter += 1
        elif fail_counter == 3:
            print("Incorrect, again. Please register again.")
            return -1
        else:
            print("Wrong. Try again.")
            fail_counter += 1
            
def print_menu():
    """
    Prints the menu for the user
    """
    print("\n####################### Main Menu:")
    print("1. Enter a purchase")
    print("2. Generate a report")
    print("3. Quit")
    result = input("Choose: ")
    while result not in ("1", "2", "3"):
        result = input("Invalid option. Try again: ")
    return result
    
def enter_purchase_date():
    """
    Asks for the purchase date. If entered correctly, it's assigned to the global variable, purchase_date.
    """
    date_entered = input("Purchase Date (MM/DD/YYYY or MM-DD-YYYY): ")
    purchase_date = None
    while purchase_date == None:
        for fmt in ('%m-%d-%Y', '%m/%d/%Y'):
            try:
                purchase_date = datetime.datetime.strptime(date_entered, fmt)
                break  # the for loop (will also prevent the else from triggering if exitted with a break.)
            except ValueError:
                pass
        else:
            date_entered = input("Invalid date format. Please enter the date in either (MM/DD/YYYY or MM-DD-YYYY) format: ")
    return purchase_date

def enter_purchase_item(purch_date: datetime.datetime):
    """
    Enter the purchase item of at least 3 characters long.
    Assigns the item in the global dictionary (purchases) for the first time, with a date + item key.

    Args:
        purch_date (datetime.datetime): the purchase date

    Returns:
        _type_: the key of the new item
    """
    while True:
        item = input("Purchased Item: ")
        if len(item) < 3:
            print("Error: Must be more than 3 characters!")
        else:
            global purchases
            key = purch_date.strftime("%Y-%m-%d") + item
            purchases[key] = {"item": item, "purch_date": purch_date}
            return key
        
def enter_item_weight(key: str):
    """
    Allows entry and saving of the item weight in kilograms, into the global purchases variable.

    Args:
        key (str): the key for the item that we're giving a weight.
    """
    weight = input("Item weight in kg (E.g 12.34): ")
    # check if float:
    while weight.isdecimal() == False and re.match(r'^-?\d+(?:\.\d+)$', weight) is None:
        weight = input("Invalid weight. Must be a float value. Try again: ")
    global purchases
    purchases[key].setdefault("weight", float(weight))
    
def enter_item_cost(key: str):
    """
    Enters the total cost into the global purchases variable. This includes the delivery costs as well.

    Args:
        key (str): the key for the item that we're giving a cost.
    """
    cost = input("Item cost in € (E.g 12.34): ")
    # check if float:
    while cost.isdecimal() == False and re.match(r'^-?\d+(?:\.\d+)$', cost) is None:
        cost = input("Invalid cost. Must be a float value. Try again: ")
    global purchases
    purchases[key].setdefault("cost", float(cost))
    
def enter_item_qty(key: str):
    """
    Allows entry and saving of the item quantity, into the global purchases variable.

    Args:
        key (str): the key for the item that we're giving a quantity.
    """
    qty = input("Item quantity (E.g 1): ")
    # check if positive int:
    while qty.isdecimal() == False or int(qty) < 1:
        qty = input("Invalid quantity. Must be a positive int value. Try again: ")
    global purchases
    purchases[key].setdefault("qty", int(qty))
    
def generate_report():
    """
    Outputs a report for the purchases
    """
    global purchases
    # 1 EURO per 1 kg
    total_kg = sum(purchases[key]["weight"] for key in purchases.keys())
    print(f"Delivery charges: {total_kg}€")
    # costs without delivery charges
    total_cost = sum(purchases[key]["cost"] for key in purchases.keys())
    without_del_charges = total_cost - total_kg
    print(f"Cost without delivery: {without_del_charges}€")
    # most and least expensive
    most_expensive = max(purchases[key]["cost"] for key in purchases.keys())
    print(f"Most expensive purchase: {most_expensive}")
    least_expensive = min(purchases[key]["cost"] for key in purchases.keys())
    print(f"Least expensive purchase: {least_expensive}")
    # average cost per order
    avg = round(sum(purchases[key]["cost"] for key in purchases.keys()) / len(purchases), 2)
    print(f"Average purchase: {avg}")
    # spending limit (500€) exceeded
    if total_cost >= 500:
        print("500€ spending limit exceeded.")
    else:
        print("500€ spending limit not exceeded.")
        
    print(f"\nReport finished, at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
    
    
#################################################  MAIN CODE:

login_registration()
input_Germany_number()
if login() == 0:
    # login was successful
    while True:
        option = print_menu()
        if len(purchases) == 0 and option == "2":
            print("You need purchases before you can generate a report :).")
        elif option == "1":
            purchase_date = enter_purchase_date()
            key = enter_purchase_item(purchase_date)
            enter_item_weight(key)
            enter_item_cost(key)
            enter_item_qty(key)
        elif option == "2":
            generate_report()
        elif option == "3":
            print("Goodbye!")
            break