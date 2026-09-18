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
inventory = 0
fail_attempt = 0
deliveries_processed = 0


while True:

    stock = get_valid_input()

    if stock == "quit":
        generate_report(inventory, fail_attempt)
        print("Total of deliveries processed:", deliveries_processed)
        break

    if stock is None:
        fail_attempt += 1
        continue

    inventory = process_delivery(inventory, stock)

    tax = calculate_tax(stock)

    deliveries_processed += 1

    print("Inventory:", inventory)
    print("Tax for this delivery:", tax)


