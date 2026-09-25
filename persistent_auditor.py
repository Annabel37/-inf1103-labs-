import os

# The data folder. Docker sets DATA_DIR to the mounted volume.
# When you run the script locally, the file is in the current folder.
DATA_DIR = os.environ.get("DATA_DIR", ".")
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.txt")


def load_inventory():
    # File format:
    # line 1 = total inventory
    # line 2 = transaction history, separated by commas
    try:
        with open(INVENTORY_FILE, "r") as file:
            lines = file.read().splitlines()
    except FileNotFoundError:
        print("No inventory file found. Starting with an empty inventory.")
        return 0, []

    try:
        total = int(lines[0]) if lines else 0
        history = []
        if len(lines) > 1 and lines[1].strip():
            history = [int(value) for value in lines[1].split(",")]
    except ValueError:
        print("Inventory file is not valid. Starting with an empty inventory.")
        return 0, []

    return total, history


# def save_inventory(total, history):
#     os.makedirs(DATA_DIR, exist_ok=True)
#     with open(INVENTORY_FILE, "w") as file:
#         file.write(str(total) + "\n")
#         file.write(",".join(str(value) for value in history) + "\n")
#     print("Inventory successfully saved to", INVENTORY_FILE)


def get_valid_input():
    while True:
        user_input = input("Enter stock (or quit): ")

        if user_input == "quit":
            return "quit"

        elif user_input.lstrip("-").isdigit():
            stock = int(user_input)

            if stock <= 0:
                print("Please enter a number greater than 0")
                return None

            return stock

        else:
            print("Please enter a number")
            return None


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    print("Total Unit Processed:", total_units)
    print("Number of failed attempts:", failed_attempts)


# Main program
inventory, history = load_inventory()
fail_attempt = 0
deliveries_processed = 0

print("Current Inventory:", inventory)
print("Transaction History:", history)
print()


while True:

    stock = get_valid_input()

    if stock == "quit":
        # save_inventory(inventory, history)
        generate_report(inventory, fail_attempt)
        print("Total of deliveries processed:", deliveries_processed)
        print("Transaction History:", history)
        break

    if stock is None:
        fail_attempt += 1
        continue

    inventory = process_delivery(inventory, stock)

    history.append(stock)

    tax = calculate_tax(stock)

    deliveries_processed += 1

    print("Inventory:", inventory)
    print("Tax for this delivery:", tax)