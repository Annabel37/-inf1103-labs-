inventory = 0
fail_attempt = 0

while True:
    user_input = input("Enter stock (or quit): ")

    if user_input == "quit":
        print("Total Unit Processed:", inventory)
        print("Number of failed attempts:", fail_attempt)
        break

# check whether is a digit, True will run the loop
    # elif user_input.isdigit():
    elif user_input.lstrip("-").isdigit():
        stock = int(user_input)

        if stock + inventory >= 500:
            print("You have exceeded the limit")
            break

        elif stock > 0:
            inventory += stock
            print("Inventory:", inventory)

        elif stock < 0:
            #wan to add the fail attempt 
            fail_attempt += 1
            print("Please enter a number greater than 0")

    else:
        fail_attempt += 1
        print("Please enter a number")    
