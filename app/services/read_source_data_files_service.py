import pandas as pd
import json
import csv


def convert_value(value):
    if value == "" or value == "nan":
        return None
    if isinstance(value, str) and value.isdigit():  # Ensure the string is numeric
        return int(value)
    try:
        return float(value) if "." in value else int(value)
    except ValueError:
        return value


def read_csv(file_path):
    try:
        with open(file_path, encoding='iso-8859-1') as file:
            reader = csv.DictReader(file)
            data = [{key: convert_value(value) for key, value in row.items()} for row in reader]
        return data
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")
