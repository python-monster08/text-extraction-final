max_validation_range = 0
def validate_yes_no(prompt):
    """ Prompt the user for a 'Y' or 'N' response and return that response. """
    while True:
        response = input(prompt).strip().upper()
        if response in ['Y', 'N']:
            return response
        else:
            print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")

def validate_number(prompt, min_val=0, max_val=10000):
    """ Prompt the user for a number within a specified range and return that number. """
    max_validation_range = max_val
    while True:
        try:
            number = int(input(prompt))
            if min_val <= number <= max_validation_range:
                return number
            else:
                print(f"Invalid input. Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
