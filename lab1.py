
def build_list():
    list = []
    while True:
        userInput = input("Enter a number or enter 'Done' to end the list: ")
        if userInput.lower() == "done":
            break
        try:
            number = float(userInput)
            list.append(number)
        except ValueError:
            print("Input invalid.")
    return list

def sort_list(unsorted_list):
    unsorted_list.sort()

def main():
    numbers = build_list()
    sort_list(numbers)
    print("Sorted list:", numbers)

main()
