#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
scan_ugly_expression.py
-----------------------
This script scans all HTML files in the project to identify "ugly" ASCII math expressions
that should be replaced with proper LaTeX notation.

The script performs the following:
1. Traverses all HTML files in the project using a graph-based approach
2. Uses pattern matching to identify potential ASCII math expressions
3. Reports files and locations containing such expressions
4. Avoids circular traversal through tracking visited nodes
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import urllib.parse

# ========== Configuration ==========

ROOT_HTML = "index.html"       # Starting point for traversal
OUTPUT_FILE = "./ugly_expressions"  # Report output location

# ========== 修改点 1：更严格的正则，增加单词边界等，避免误匹配标签属性或子串 ==========

ASCII_MATH_PATTERNS = [
    # x * y
    r'\b[a-zA-Z0-9_]+\s*\*\s*[a-zA-Z0-9_]+\b',
    # x / y
    r'\b[a-zA-Z0-9_]+\s*/\s*[a-zA-Z0-9_]+\b',
    # x ^ y
    r'\b[a-zA-Z0-9_]+\s*\^\s*[a-zA-Z0-9_]+\b',
    # sum(...)
    r'sum\s*\([^\)]*\)',
    # max{...} or min{...}
    r'max\s*\{[^\}]*\}',
    r'min\s*\{[^\}]*\}',
    # x_1 (etc.)
    r'\b[a-zA-Z]+_[0-9]+\b',
    # 更严格排除 path-norm / seminorm 等带前后缀的情况
    #r'(?<!\\)(?<![A-Za-z0-9_\-])norm(?![A-Za-z0-9_\-])',
    # |x| not in LaTeX
    r'\|[a-zA-Z0-9_]+\|',
]

# Exclusion areas - don't check these tags for math expressions
EXCLUDED_TAGS = ['script', 'style', 'code', 'pre']

# ========== Global variables ==========
visited = set()              # Tracks visited HTML files (absolute paths)
ugly_expressions = {}        # Dictionary: {filename: [(context, line_number, pattern_matched)]}

# ========== Helper functions ==========

def normalize_path(base_path, link_path):
    """
    Convert relative link to absolute path for local files.
    """
    base_dir = os.path.dirname(base_path)
    joined = urllib.parse.urljoin("file://" + base_dir + "/", link_path)
    abs_path = joined.replace("file://", "")
    return os.path.abspath(abs_path)

def extract_local_html_links(file_path):
    """
    Extract all local HTML links from a file.
    Returns (existing_links, missing_links)
    """
    existing_links = []
    missing_links = []
    
    if not os.path.isfile(file_path):
        return existing_links, missing_links

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all <a href="..."> tags
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href'].strip()
        # Check for local .html files (exclude external links)
        if '.html' in href and not href.lower().startswith(('http://', 'https://')):
            abs_target = normalize_path(file_path, href)
            if os.path.isfile(abs_target):
                existing_links.append(abs_target)
            else:
                # File doesn't exist (broken link)
                link_text = a_tag.get_text(strip=True)
                missing_links.append((href, link_text))
    
    return existing_links, missing_links

# ========== 修改点 2：统一通过“get_text()”只获取可见文本 ==========

def get_visible_text_excluding_tags(html_content):
    """
    Use BeautifulSoup to remove EXCLUDED_TAGS, then get only visible text via .get_text().
    This way, we skip HTML tags/attributes, avoiding false matches like "rel='stylesheet'/".
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in EXCLUDED_TAGS:
        for excluded in soup.find_all(tag):
            excluded.decompose()
    # Now get only visible text (no HTML attributes)
    return soup.get_text()

# ========== 修改点 3：识别数学环境的掩码，用于在纯文本中判断是否在 $...$ 或 $$...$$ ==========

def build_math_mode_mask(text):
    """
    Build a boolean mask array (same length as text),
    where True means "this character is inside a LaTeX math environment ($ or $$)".
    """
    in_math_mode = [False] * len(text)
    i = 0
    in_inline = False   # $...$ 
    in_display = False  # $$...$$
    length = len(text)
    
    while i < length:
        if text.startswith('$$', i):
            in_display = not in_display
            # Mark these two '$$' as math mode (if you want)
            for k in range(i, i+2):
                if k < length:
                    in_math_mode[k] = in_display or in_inline
            i += 2
        elif text[i] == '$':
            in_inline = not in_inline
            in_math_mode[i] = in_display or in_inline
            i += 1
        else:
            if in_display or in_inline:
                in_math_mode[i] = True
            i += 1
    return in_math_mode

def check_for_ugly_expressions(file_path):
    """
    Scan HTML file for ASCII math expressions. Return list of (context, line_number, pattern_matched).
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 1) 取可见文本（忽略标签和属性），避免匹配到 HTML 的 <...> 中
    visible_text = get_visible_text_excluding_tags(html_content)
    
    # 2) 构建数学环境掩码
    math_mask = build_math_mode_mask(visible_text)
    
    # 3) 我们把文本按行分割，以便报告“行号”和“上下文”
    lines = visible_text.split('\n')
    
    # 计算每行在 visible_text 里的 global offset
    line_start_positions = []
    offset = 0
    for line in lines:
        line_start_positions.append(offset)
        offset += len(line) + 1  # +1 for the newline char removed by split
    
    found_expressions = []
    
    # 4) 针对每行、每条 pattern 做匹配
    for pattern in ASCII_MATH_PATTERNS:
        regex = re.compile(pattern)
        for i, line in enumerate(lines):
            for m in regex.finditer(line):
                global_start = line_start_positions[i] + m.start()
                # 如果匹配位置在数学环境中，则跳过
                if math_mask[global_start]:
                    continue
                # 否则，记录该可疑表达式
                context = line
                line_number = i + 1
                found_expressions.append((context, line_number, pattern))
    return found_expressions

def add_ugly_expressions(filename, expressions):
    """
    Add found expressions to the global tracker.
    """
    if expressions:
        ugly_expressions[filename] = expressions

def dfs_scan(file_path):
    """
    Depth-first scan of HTML files from given path.
    Checks for ASCII math expressions and follows local links.
    """
    if file_path in visited:
        return
    visited.add(file_path)
    
    filename = os.path.basename(file_path)
    expressions = check_for_ugly_expressions(file_path)
    if expressions:
        add_ugly_expressions(filename, expressions)
    
    existing_links, _ = extract_local_html_links(file_path)
    for link in existing_links:
        dfs_scan(link)

# ========== Main logic ==========

def main():
    root_path = os.path.abspath(ROOT_HTML)
    if os.path.isfile(root_path):
        dfs_scan(root_path)
    else:
        print(f"Warning: Root file {ROOT_HTML} doesn't exist, cannot start scanning.")
    
    # Also check for "orphaned" HTML files not linked from anywhere
    all_htmls = list(Path(".").rglob("*.html"))
    for html_file in all_htmls:
        abs_file = os.path.abspath(html_file)
        if abs_file not in visited:
            dfs_scan(abs_file)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        if ugly_expressions:
            out_file.write(f"Scan complete. Found potential ASCII math expressions in {len(ugly_expressions)} files:\n\n")
            for fname, expressions in ugly_expressions.items():
                out_file.write(f"File: {fname}\n")
                out_file.write(f"Found {len(expressions)} potential issues:\n")
                for idx, (context, line_number, pattern) in enumerate(expressions, 1):
                    out_file.write(f"  {idx}. Line {line_number}: {context.strip()}\n")
                    out_file.write(f"     Matched pattern: {pattern}\n")
                out_file.write("\n")
            out_file.write("\nRecommendation: Replace these expressions with proper LaTeX notation within $ or $$ delimiters.\n")
        else:
            out_file.write("Scan complete. No potential ASCII math expressions found.\n")
    
    print(f"Scan complete. Results written to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
