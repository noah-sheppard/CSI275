"""Lab 3, Adding Socket Sorting to Lab 1.

Author: Noah Sheppard
Class: CSI-275-01
Assignment: Lab 3: Socket Sorting

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)
"""

import socket

def build_list():
    """Collect input from the user and return it as a list.

    Only numeric input will be included; strings are rejected.
    """
    #Create a list to store our numbers
    unsorted_list = []

    # Create a variable for input
    user_input = ""

    while user_input != "done":
        # Prompt the user for input
        user_input = input("Please enter a number, or 'done' to stop.")

        # Validate our input, and add it to out list
        # if it's a number
        try:
            # Were we given an integer?
            unsorted_list.append(int(user_input))
        except ValueError:
            try:
                # Were we given a floating-point number?
                unsorted_list.append(float(user_input))
            except ValueError:
                # Non-numeric input - if it's not "done",
                # reject it and move on
                if (user_input != "done"):
                    print ("ERROR: Non-numeric input provided.")
                continue

    # Once we get here, we're done - return the list
    return unsorted_list

def sort_list(unsorted_list):
    """Send the unsorted list to the CSI-275 sorting server and prints
    the sorted result from the server.
    """
    server_ip_address = "159.203.166.188"
    server_port_number = 7778

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.connect((server_ip_address, server_port_number))

        str_of_list = "LIST " + " ".join(map(str, unsorted_list))

        server_socket.send(str_of_list.encode("ascii"))

        response_from_server = server_socket.recv(1024).decode("ascii")

        print("Server response:", response_from_server)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server_socket.close()
    pass

def main():
    """Call the build_list and sort_list functions, and print the result."""
    number_list = build_list()
    sort_list(number_list)

if __name__ == "__main__":
    main()

