# Phone Number Normalizer

A small CLI tool that reads a tab-separated text file of names + phone numbers, normalizes the numbers, and prints them in a consistent format:

(AAA) BBB-CCCC    Name

It supports phone numbers written with:
- punctuation (spaces, dashes, dots, underscores, bullets, etc.)
- a leading US country code `1`
- “phonewords” (letters mapped to digits, e.g., 425-TULIPS-2)

## Input format

Each line must be:

Name<TAB>PhoneNumber

Example:

Benjamin Sosa    1 (825) 828-0003

## Output format

The program prints:

(825) 828-0003    Benjamin Sosa

If a line cannot be normalized into a valid 10-digit NANP phone number, it prints:

[Invalid: <original input>]    Name

## Validation rules

After converting letters → digits and removing symbols:
- A leading country code `1` is allowed only if the cleaned number has 11 digits (it will be stripped).
- The final number must be exactly 10 digits.
- Area code and exchange code cannot start with `0` or `1`.
- Certain “reserved-looking” patterns are rejected (e.g., codes ending in `11`), based on project rules.

## How to run

```bash
python phone_numbers.py sample_phone_numbers.txt
