#!/usr/bin/env python3
import os
import re

def check_mathjax_in_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Check if the path is correctly set to ../js/mathjax-config.js for nodes
    if 'nodes/' in file_path:
        config_path_correct = '../js/mathjax-config.js' in content
        path_message = "✅ Correct config path" if config_path_correct else "❌ Incorrect config path"
    else:
        config_path_correct = 'js/mathjax-config.js' in content
        path_message = "✅ Correct config path" if config_path_correct else "❌ Incorrect config path"
    
    # Check if using the correct MathJax script source
    script_source_correct = 'src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"' in content
    script_message = "✅ Correct script source" if script_source_correct else "❌ Incorrect script source"
    
    print(f"{file_path}:")
    print(f"  {path_message}")
    print(f"  {script_message}")
    
    return config_path_correct and script_source_correct

def process_directory(directory):
    all_correct = True
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if not check_mathjax_in_file(file_path):
                    all_correct = False
    
    return all_correct

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    nodes_dir = os.path.join(base_dir, 'nodes')
    index_path = os.path.join(base_dir, 'index.html')
    
    # Check index file
    print("Checking index file...")
    index_correct = check_mathjax_in_file(index_path)
    
    # Check all node files
    print("\nChecking node files...")
    nodes_correct = process_directory(nodes_dir)
    
    # Overall result
    if index_correct and nodes_correct:
        print("\n✅ All MathJax configurations are correct!")
    else:
        print("\n❌ Some MathJax configurations need fixing. See details above.")
