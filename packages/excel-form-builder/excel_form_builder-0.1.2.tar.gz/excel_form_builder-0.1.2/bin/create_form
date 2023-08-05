#!/usr/bin/python
import argparse
from excel_form_builder import ExcelToJson
from openpyxl import load_workbook
from colorama import init

def main():
    parser = argparse.ArgumentParser(description="Excel workbook to JSON")
    parser.add_argument('filename', type=str, help="Name of file")
    args = parser.parse_args()

    workbook = load_workbook(filename=args.filename, read_only=True)
    form_name = args.filename[:-5]
    worksheet = workbook.worksheets[0]

    init(autoreset=True) #Colorama
    
    ExcelToJson(worksheet, form_name).create_form()
    return

if __name__ == "__main__":
    main()
