import re
from argparse import ArgumentParser
import sys

LETTER_TO_NUMBER = {
    'A': '2', 'B': '2', 'C': '2',
    'D': '3', 'E': '3', 'F': '3',
    'G': '4', 'H': '4', 'I': '4',
    'J': '5', 'K': '5', 'L': '5',
    'M': '6', 'N': '6', 'O': '6',
    'P': '7', 'Q': '7', 'R': '7', 'S': '7',
    'T': '8', 'U': '8', 'V': '8',
    'W': '9', 'X': '9', 'Y': '9', 'Z': '9'
}


class PhoneNumber:
    """ Represents a phone number

    Attributes:
        area_code(str): Area code of the number
        exchange_code(str): Exchange code of the number
        line_number(str): Line number of the phone number
    """
    def __init__(self, area_code, exchange_code, line_number):
        """ Initializes PhoneNumber object with the parts of phone number.

        Args:
            area_code(str): Area code of the number
            exchange_code(str): Exchange code of the number
            line_number(str): Line number of the phone number
        """
        self.area_code = area_code
        self.exchange_code = exchange_code
        self.line_number = line_number
        self.number = f"{area_code}{exchange_code}{line_number}"

        if self.area_code[0] in ('0', '1') or \
           self.exchange_code[0] in ('0', '1') or \
           self.area_code.endswith('11') or \
           self.line_number.endswith('11'):
            raise ValueError("Error: area or exchange code")

    def __int__(self):
        """Returns an integer version of phone number"""
        return int(self.number)

    def __repr__(self):
        """Returns string version of phone number"""
        return f"PhoneNumber('{self.number}')"

    def __str__(self):
        """Returns formatted string version of phone number"""
        return f"({self.area_code}) {self.exchange_code}-{self.line_number}"

    def __lt__(self, other):
        """Compares two numbers"""
        return int(self) < int(other)

    def __gt__(self, other):
        """Compares two numbers"""
        return int(self) > int(other)


def normalize_number(number):
    """Normalizes a phone number string.

    Args:
        number (str): Raw phone number input that may include letters and symbols

    Returns:
        str: Cleaned string of digits with letters converted, symbols removed,
             and leading country code stripped
    """
    number = ''.join(LETTER_TO_NUMBER.get(char.upper(), char) for char in number)
    number = re.sub(r'\D', '', number)
    if len(number) > 10 and number.startswith('1'):
        number = number[1:]
    return number


def read_numbers(path):
    """Reads the numbers from txt file and changes them to the right format

    Args:
        path(str): Path to text file

    Returns:
        phone_numbers(list): list of names and phone numbers (formatted or marked invalid)
    """
    phone_numbers = []
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            info = line.strip().split('\t')
            if len(info) < 2:
                continue
            name = info[0]
            raw_number = info[1]
            number = normalize_number(raw_number)

            if len(number) >= 10:
                number = number[-10:]
                area_code = number[:3]
                exchange_code = number[3:6]
                line_number = number[6:]
                fixed = f"({area_code}) {exchange_code}-{line_number}"
                phone_numbers.append((name, fixed))
            else:
                phone_numbers.append((name, f"[Invalid: {raw_number}]"))

    return phone_numbers


def main(path):
    """Read data from path and print results.

    Args:
        path (str): path to a text file. Each line in the file should consist of
            a name, a tab character, and a phone number.

    Side effects:
        Writes to stdout.
    """
    for name, number in read_numbers(path):
        print(f"{number}\t{name}")


def parse_args(arglist):
    """Parse command-line arguments.

    Expects one mandatory command-line argument: a path to a text file where
    each line consists of a name, a tab character, and a phone number.

    Args:
        arglist (list of str): a list of command-line arguments to parse.

    Returns:
        argparse.Namespace: a namespace object with a file attribute whose value
        is a path to a text file as described above.
    """
    parser = ArgumentParser()
    parser.add_argument("file", help="file of names and numbers")
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.file)
