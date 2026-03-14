#Budget Planner Program


#Main menu section
def main():
    user_choice = ""

    while user_choice != "4":
        print("\n=== Budget Planner Main Menu ===")
        print("1. Build a Budget")
        print("2. Calculate Discounts")
        print("3. Sort Money Into Groups")
        print("4. Exit")

        user_choice = input("Enter your choice: ")

        if user_choice == "1":
            build_budget()
        elif user_choice == "2":
            calculate_discount_menu()
        elif user_choice == "3":
            sort_money()
        elif user_choice == "4":
            print("Thank you for using the Budget Planner Program.")
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")


#Function for formatting money
def money_format(amount):
    return "$" + format(amount, ".2f")


#Data collection section for decimal numbers
def get_float_input(prompt_text):
    while True:
        try:
            number_entered = float(input(prompt_text))
            if number_entered < 0:
                print("Please enter a number that is 0 or higher.")
            else:
                return number_entered
        except ValueError:
            print("Invalid input. Please enter a valid number.")


#Data collection section for whole numbers
def get_int_input(prompt_text):
    while True:
        try:
            whole_number_entered = int(input(prompt_text))
            if whole_number_entered < 0:
                print("Please enter a whole number that is 0 or higher.")
            else:
                return whole_number_entered
        except ValueError:
            print("Invalid input. Please enter a valid whole number.")


#Data collection section for percentages
def get_percentage_input(prompt_text):
    while True:
        try:
            percentage_entered = float(input(prompt_text))
            if percentage_entered < 0 or percentage_entered > 100:
                print("Please enter a percentage from 0 to 100.")
            else:
                return percentage_entered
        except ValueError:
            print("Invalid input. Please enter a valid percentage.")


#Data collection section for yes or no
def get_yes_no_input(prompt_text):
    while True:
        yes_no_answer = input(prompt_text).strip().lower()

        if yes_no_answer == "yes" or yes_no_answer == "y":
            return "yes"
        elif yes_no_answer == "no" or yes_no_answer == "n":
            return "no"
        else:
            print("Please answer yes or no.")


#Data collection section for budget period
def get_budget_period():
    while True:
        print("\nChoose your budget period:")
        print("1. Weekly")
        print("2. Bi-Weekly")
        print("3. Monthly")

        period_choice = input("Enter your choice: ")

        if period_choice == "1":
            return "Weekly"
        elif period_choice == "2":
            return "Bi-Weekly"
        elif period_choice == "3":
            return "Monthly"
        else:
            print("Invalid choice. Please select 1, 2, or 3.")


#Build budget section
def build_budget():
    print("\n--- Build a Budget ---")

    #Data collection section
    budget_period = get_budget_period()
    total_money_available = get_float_input("How much money do you currently have for this " + budget_period + " period? ")
    savings_percentage = get_percentage_input("What percentage would you like to save? ")

    food_cost = get_float_input("How much do you spend on food for this " + budget_period + " period? ")
    bills_cost = get_float_input("How much do you spend on bills for this " + budget_period + " period? ")
    essentials_cost = get_float_input("How much do you spend on essentials for this " + budget_period + " period? ")

    #Calculation section
    planned_savings_amount = total_money_available * (savings_percentage / 100)

    #Custom category section
    custom_categories = []
    custom_category_total = 0

    add_custom_category = get_yes_no_input("Would you like to add custom budget categories? (yes/no): ")

    while add_custom_category == "yes":
        category_name = input("Enter the custom category name: ")
        category_amount = get_float_input("How much money goes to " + category_name + "? ")

        custom_categories.append([category_name, category_amount])
        custom_category_total = custom_category_total + category_amount

        add_custom_category = get_yes_no_input("Would you like to add another custom category? (yes/no): ")

    #Savings account section
    savings_account_list = []
    savings_account_total = 0

    has_savings_accounts = get_yes_no_input("Do you have any savings accounts? (yes/no): ")

    if has_savings_accounts == "yes":
        number_of_accounts = get_int_input("How many savings accounts do you have? ")

        account_counter = 1
        while account_counter <= number_of_accounts:
            account_name = input("Enter the name of savings account #" + str(account_counter) + ": ")
            account_amount = get_float_input("How much money is going into " + account_name + "? ")

            savings_account_list.append([account_name, account_amount])
            savings_account_total = savings_account_total + account_amount

            account_counter = account_counter + 1

    #Calculation section
    basic_budget_total = food_cost + bills_cost + essentials_cost
    tied_up_total = basic_budget_total + planned_savings_amount + custom_category_total + savings_account_total
    liquid_money_remaining = total_money_available - tied_up_total

    food_percent = calculate_category_percent(food_cost, total_money_available)
    bills_percent = calculate_category_percent(bills_cost, total_money_available)
    essentials_percent = calculate_category_percent(essentials_cost, total_money_available)
    savings_percent = calculate_category_percent(planned_savings_amount, total_money_available)
    custom_percent = calculate_category_percent(custom_category_total, total_money_available)
    account_percent = calculate_category_percent(savings_account_total, total_money_available)
    liquid_percent = calculate_category_percent(liquid_money_remaining, total_money_available)

    #Summary text section
    summary_text = ""
    summary_text = summary_text + "\n--- Budget Summary ---\n"
    summary_text = summary_text + "Budget Period: " + budget_period + "\n"
    summary_text = summary_text + "Total Money Available: " + money_format(total_money_available) + "\n"
    summary_text = summary_text + "Planned Savings: " + money_format(planned_savings_amount) + " (" + format(savings_percent, ".2f") + "%)\n"
    summary_text = summary_text + "Food: " + money_format(food_cost) + " (" + format(food_percent, ".2f") + "%)\n"
    summary_text = summary_text + "Bills: " + money_format(bills_cost) + " (" + format(bills_percent, ".2f") + "%)\n"
    summary_text = summary_text + "Essentials: " + money_format(essentials_cost) + " (" + format(essentials_percent, ".2f") + "%)\n"
    summary_text = summary_text + "Custom Categories Total: " + money_format(custom_category_total) + " (" + format(custom_percent, ".2f") + "%)\n"
    summary_text = summary_text + "Savings Accounts Total: " + money_format(savings_account_total) + " (" + format(account_percent, ".2f") + "%)\n"
    summary_text = summary_text + "Total Tied Up Money: " + money_format(tied_up_total) + "\n"
    summary_text = summary_text + "Liquid Money Remaining: " + money_format(liquid_money_remaining) + " (" + format(liquid_percent, ".2f") + "%)\n"

    if liquid_money_remaining < 0:
        summary_text = summary_text + "\nWarning: You have assigned more money than you currently have.\n"

    if len(custom_categories) > 0:
        summary_text = summary_text + "\nCustom Category Breakdown:\n"
        for one_category in custom_categories:
            summary_text = summary_text + one_category[0] + ": " + money_format(one_category[1]) + "\n"

    if len(savings_account_list) > 0:
        summary_text = summary_text + "\nSavings Account Breakdown:\n"
        for one_account in savings_account_list:
            summary_text = summary_text + one_account[0] + ": " + money_format(one_account[1]) + "\n"

    #Print out section
    print(summary_text)

    #File save section
    save_summary = get_yes_no_input("Would you like to save this budget summary to a file? (yes/no): ")

    if save_summary == "yes":
        file_name = input("Enter a file name such as budget_summary.txt: ")
        save_text_to_file(file_name, summary_text)


#Calculation section for category percentages
def calculate_category_percent(category_amount, total_amount):
    if total_amount == 0:
        return 0
    else:
        return (category_amount / total_amount) * 100


#Discount menu section
def calculate_discount_menu():
    print("\n--- Calculate Discounts ---")

    keep_calculating = "yes"
    discount_summary_text = "\n--- Discount Summary ---\n"
    discount_counter = 1

    while keep_calculating == "yes":
        #Data collection section
        item_name = input("Enter the name of the item: ")
        original_price = get_float_input("Enter the original price of the item: ")
        discount_percent = get_percentage_input("Enter the discount percentage: ")

        #Calculation section
        discount_amount = original_price * (discount_percent / 100)
        final_price = original_price - discount_amount
        deal_message = get_deal_message(discount_percent)

        #Print out section
        print("\nItem:", item_name)
        print("Original Price:", money_format(original_price))
        print("Discount Percent:", str(discount_percent) + "%")
        print("You Save:", money_format(discount_amount))
        print("Final Price:", money_format(final_price))
        print("Deal Rating:", deal_message)

        discount_summary_text = discount_summary_text + "\nItem #" + str(discount_counter) + "\n"
        discount_summary_text = discount_summary_text + "Item Name: " + item_name + "\n"
        discount_summary_text = discount_summary_text + "Original Price: " + money_format(original_price) + "\n"
        discount_summary_text = discount_summary_text + "Discount Percent: " + str(discount_percent) + "%\n"
        discount_summary_text = discount_summary_text + "Discount Amount: " + money_format(discount_amount) + "\n"
        discount_summary_text = discount_summary_text + "Final Price: " + money_format(final_price) + "\n"
        discount_summary_text = discount_summary_text + "Deal Rating: " + deal_message + "\n"

        discount_counter = discount_counter + 1
        keep_calculating = get_yes_no_input("Would you like to calculate another discount? (yes/no): ")

    #File save section
    save_summary = get_yes_no_input("Would you like to save this discount summary to a file? (yes/no): ")

    if save_summary == "yes":
        file_name = input("Enter a file name such as discount_summary.txt: ")
        save_text_to_file(file_name, discount_summary_text)


#Deal rating section
def get_deal_message(discount_percent):
    if discount_percent < 10:
        return "Small discount"
    elif discount_percent < 25:
        return "Decent deal"
    elif discount_percent < 50:
        return "Good deal"
    else:
        return "Excellent deal"


#Sort money section
def sort_money():
    print("\n--- Sort Money Into Groups ---")

    #Data collection section
    total_money_to_sort = get_float_input("How much money do you want to sort? ")

    sorted_group_list = []
    total_sorted_amount = 0
    group_counter = 1
    keep_sorting = "yes"

    while keep_sorting == "yes":
        default_group_name = get_group_letter_name(group_counter)
        use_default_name = get_yes_no_input("Would you like to use default group name " + default_group_name + "? (yes/no): ")

        if use_default_name == "yes":
            group_name = default_group_name
        else:
            group_name = input("Enter a custom group name: ")

        group_amount = get_float_input("How much money goes into " + group_name + "? ")

        sorted_group_list.append([group_name, group_amount])
        total_sorted_amount = total_sorted_amount + group_amount

        if total_sorted_amount > total_money_to_sort:
            print("Warning: You have sorted more money than you started with.")

        keep_sorting = get_yes_no_input("Are there more groups? (yes/no): ")
        group_counter = group_counter + 1

    #Calculation section
    remaining_money = total_money_to_sort - total_sorted_amount

    #Summary text section
    summary_text = ""
    summary_text = summary_text + "\n--- Sorting Summary ---\n"
    summary_text = summary_text + "Starting Money: " + money_format(total_money_to_sort) + "\n"
    summary_text = summary_text + "Total Sorted: " + money_format(total_sorted_amount) + "\n"
    summary_text = summary_text + "Remaining Money: " + money_format(remaining_money) + "\n"

    if remaining_money < 0:
        summary_text = summary_text + "\nWarning: You assigned more money than you started with.\n"

    summary_text = summary_text + "\nMoney Sorted Into Groups:\n"
    for one_group in sorted_group_list:
        summary_text = summary_text + one_group[0] + ": " + money_format(one_group[1]) + "\n"

    #Print out section
    print(summary_text)

    #File save section
    save_summary = get_yes_no_input("Would you like to save this sorting summary to a file? (yes/no): ")

    if save_summary == "yes":
        file_name = input("Enter a file name such as sorting_summary.txt: ")
        save_text_to_file(file_name, summary_text)


#Group name section
def get_group_letter_name(group_counter):
    if group_counter <= 26:
        return "Group " + chr(64 + group_counter)
    else:
        return "Group " + str(group_counter)


#File writing section
def save_text_to_file(file_name, summary_text):
    try:
        output_file = open(file_name, "w")
        output_file.write(summary_text)
        output_file.close()
        print("Summary saved successfully to", file_name)
    except:
        print("There was a problem saving the file.")


#Calling main function
main()