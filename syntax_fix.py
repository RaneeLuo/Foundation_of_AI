# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 23:48:07 2024

@author: Calan
"""

file_path = r"C:\Users\Calan\Documents\CodeProjects\FoundationOfAI\competitive_sudoku\team25_A1\sudokuai.py"

# Read and clean the file
with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

# Replace non-breaking spaces
cleaned_content = content.replace("\u00A0", " ")

# Write back the cleaned content
with open(file_path, "w", encoding="utf-8") as file:
    file.write(cleaned_content)

print("File cleaned successfully!")
