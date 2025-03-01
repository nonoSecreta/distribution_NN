#!/usr/bin/env python3
import os
import re

def fix_paths_in_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Fix MathJax script paths - change ../../js/mathjax-config.js to ../js/mathjax-config.js
    updated_content = content.replace('../../js/mathjax-config.js', '../js/mathjax-config.js')
    
    # Only write back if changes were made
    if updated_content != content:
        with open(file_path, 'w') as file:
            file.write(updated_content)
        return True
    return False

def process_directory(directory):
    files_updated = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if fix_paths_in_file(file_path):
                    files_updated += 1
                    print(f"Updated: {file_path}")
    
    return files_updated

if __name__ == "__main__":
    nodes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nodes')
    files_updated = process_directory(nodes_dir)
    print(f"Total files updated: {files_updated}")
