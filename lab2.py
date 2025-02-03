"""Lab 2, hosts implementation.

Author: Noah Sheppard
Class: CSI-275-01
Assignment: Lab 2: Host Names and IP Addresses

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

import re


"""Student code for Lab/HW1.

    Run python autograder.py

Champlain College CSI-235, Spring 2019
The following code was written by Joshua Auerbach (jauerbach@champlain.edu)
Host class __init__ function by Jason Reeves 1/4/2021 (reeves@champlain.edu)
"""


class InvalidEntryError(Exception):
    """Exception raised for invalid entries in the hosts file."""

    pass


def is_valid_ip_address(ip_address):
    """Return whether the given ip_address is a valid IPv4 address or not.

    Args:
        ip_address (str): ip_address to test

    Returns:
        bool: True if ip_address is valid IPv4 address, False otherwise.
    """
    if not isinstance(ip_address, str):
        return False
    ip_pattern = re.compile(
        r"^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.)"
        r"{3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$"
    )
    return bool(ip_pattern.match(ip_address))


def is_valid_hostname(hostname):
    """Return whether the given hostname is valid or not.

    Host names may contain only alphanumeric characters, minus signs ("-"),
    and periods ("."). They must begin with an alphabetic character and end
    with an alphanumeric character.

    Args:
        hostname (str): hostname to test

    Returns:
        bool: True if hostname is valid, False otherwise.
    """
    if not hostname:
        return False
    hostname_pattern = re.compile(
        r"^[a-zA-Z]([a-zA-Z0-9\-\.]*[a-zA-Z0-9])?$"
    )
    return bool(hostname_pattern.match(hostname))


class Hosts:
    """The Hosts class handles translating hostnames to IP addresses."""

    def __init__(self, hosts_file):
        """Initialize the Hosts class.

        Imports all of the host names and addresses
        from the provided hosts_file.
        If the file does not follow the proper format or
        contains invalid IP addresses,
        hostnames, or aliases, an InvalidEntryError is raised.

        Args:
            hosts_file (str): Path to the hosts file.

        Raises:
            InvalidEntryError: If the file contains invalid entries.
        """
        self.ips = []
        self.hostnames = []

        with open(hosts_file, "r") as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith("#"):
                    continue

                # Split the line into parts
                parts = line.split()
                if not parts:
                    continue

                # The first part is the IP address
                ip_address = parts[0]
                if not is_valid_ip_address(ip_address):
                    raise InvalidEntryError(
                        f"Invalid IP address: {ip_address}"
                    )

                # The remaining parts are hostnames and aliases
                for hostname in parts[1:]:
                    if hostname.startswith("#"):
                        break  # Stop processing if a comment is encountered
                    if not is_valid_hostname(hostname):
                        raise InvalidEntryError(
                            f"Invalid hostname: {hostname}"
                        )
                    self.ips.append(ip_address)
                    self.hostnames.append(hostname)

    def contains_entry(self, hostname):
        """Return whether or not a given hostname exists.

        Args:
            hostname (str): Hostname to check.

        Returns:
            bool: True if the hostname exists, False otherwise.
        """
        return hostname in self.hostnames

    def get_ip(self, hostname):
        """Return the IP for a given hostname.

        Args:
            hostname (str): Hostname to look up.

        Returns:
            str: The corresponding IP address, or None if not found.
        """
        for i, name in enumerate(self.hostnames):
            if name == hostname:
                return self.ips[i]
        return None
