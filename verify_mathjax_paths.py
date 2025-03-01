#!/usr/bin/env python3
import os
import re

def check_path_in_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Check if the path is correctly set to ../js/mathjax-config.js
    if '../../js/mathjax-config.js' in content:
        print(f"❌ Incorrect path in: {file_path}")
        return False
    elif '../js/mathjax-config.js' in content:
        print(f"✅ Correct path in: {file_path}")
        return True
    else:
        print(f"⚠️ No MathJax config path found in: {file_path}")
        return None

def process_directory(directory):
    correct_files = 0
    incorrect_files = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                result = check_path_in_file(file_path)
                if result is True:
                    correct_files += 1
                elif result is False:
                    incorrect_files += 1
    
    return correct_files, incorrect_files

if __name__ == "__main__":
    nodes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nodes')
    correct, incorrect = process_directory(nodes_dir)
    print(f"\nSummary:\n- Correct paths: {correct}\n- Incorrect paths: {incorrect}")
