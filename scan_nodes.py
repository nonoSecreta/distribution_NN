#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
scan_nodes.py
-------------
本脚本从 index.html 出发，递归扫描所有通过 <a href="xxx.html"> 链接到的本地 HTML 文件，
检查这些文件中是否缺失了特定的几个区域（对于一般节点：Motivation、Example；对于 index.html：多一个 Overview）。
如果项目中还有其他未被链接到的 .html 文件，也会一并检查。
此外，还会检查出"链接指向的 HTML 文件实际并不存在"这种情况，将其也写到输出结果中。
扫描结果输出到 empty_nodes 文件。
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import urllib.parse

# ========== 配置项 ==========

ROOT_HTML = "index.html"       # 知识网络的根入口文件
OUTPUT_FILE = "./empty_nodes"  # 扫描结果输出文件

# 简单判断是否是"占位符"文本的参数
MIN_CONTENT_LENGTH = 50
PLACEHOLDER_PATTERNS = [
    r"TODO",
    r"PLACEHOLDER",
    r"TO BE COMPLETED",
    r"COMING SOON",
    r"UNDER CONSTRUCTION"
]

# ========== 全局变量 ==========
visited = set()      # 已访问过的文件（存绝对路径）
empty_nodes = {}     # { filename: [list of issues] }

# ========== 工具函数 ==========

def is_placeholder_text(text):
    """
    判断文本是否过短或匹配典型的占位符模式。
    """
    if not text or len(text.strip()) < MIN_CONTENT_LENGTH:
        return True
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def normalize_path(base_path, link_path):
    """
    将相对链接 link_path 转成绝对路径（针对本地文件）。
    方便后续判断和去重。
    """
    base_dir = os.path.dirname(base_path)
    # 用 urljoin 拼接可能的相对路径
    joined = urllib.parse.urljoin("file://" + base_dir + "/", link_path)
    # 转为绝对系统路径
    abs_path = joined.replace("file://", "")
    abs_path = os.path.abspath(abs_path)
    return abs_path

def extract_local_html_links(file_path):
    """
    解析 file_path 指向的 HTML 文件，找出所有本地 .html 链接。
    返回 (existing_links, missing_links) 两部分：
      - existing_links: 文件确实存在的本地 HTML 的绝对路径列表
      - missing_links:  文件不存在的本地 HTML 链接信息列表，元素为 (href, link_text)
    """
    existing_links = []
    missing_links = []
    if not os.path.isfile(file_path):
        return existing_links, missing_links

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')

    # 找所有 <a href="..."> 标签
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href'].strip()
        # 简单判断本地的 .html 文件（排除 http:// 和 https://）
        if '.html' in href and not href.lower().startswith(('http://', 'https://')):
            abs_target = normalize_path(file_path, href)
            if os.path.isfile(abs_target):
                existing_links.append(abs_target)
            else:
                # 文件不存在，记录为 missing_links
                link_text = a_tag.get_text(strip=True)
                missing_links.append((href, link_text))

    return existing_links, missing_links

def check_node_file(file_path):
    """
    检查单个 HTML 文件里是否缺少特定 section。
    返回 (filename, issues)。
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')

    filename = os.path.basename(file_path)
    issues = []

    # 是否是 index.html
    is_index = (filename == "index.html")

    # 1. Motivation
    motivation_header = soup.find('h2', string=re.compile(r"Motivation", re.IGNORECASE))
    if motivation_header:
        # 收集到下一个 <h2> 或到文档末尾前的 <p> 内容
        motivation_text = ""
        for sibling in motivation_header.next_siblings:
            if sibling.name == 'h2':
                break
            if sibling.name == 'p':
                motivation_text += sibling.get_text() + " "
        if is_placeholder_text(motivation_text):
            issues.append("Motivation 内容过少或疑似占位符")
    else:
        issues.append("缺少 Motivation 区域")

    # 2. 如果是 index.html，还要检查 Overview
    if is_index:
        overview_header = soup.find('h2', string=re.compile(r"Overview", re.IGNORECASE))
        if overview_header:
            overview_text = ""
            for sibling in overview_header.next_siblings:
                if sibling.name == 'h2':
                    break
                if sibling.name == 'p':
                    overview_text += sibling.get_text() + " "
            if is_placeholder_text(overview_text):
                issues.append("Overview 内容过少或疑似占位符")
        else:
            issues.append("index.html 缺少 Overview 区域")

    # 3. Example
    example_box = soup.select_one('.example-box')
    if example_box:
        if is_placeholder_text(example_box.get_text()):
            issues.append("Example 内容过少或疑似占位符")
    else:
        issues.append("缺少 Example 区域")

    return filename, issues

def add_issue_to_empty_nodes(filename, issue):
    """
    辅助函数：为某个文件名记录一个问题。
    """
    if filename not in empty_nodes:
        empty_nodes[filename] = []
    empty_nodes[filename].append(issue)

def dfs_scan(file_path):
    """
    DFS 扫描指定 HTML 文件：
    1) 检查内容是否缺少必需的 section；
    2) 找出子链接并继续 DFS；
    3) 若发现链接对应的文件并不存在，则记录为问题。
    """
    # 如果已访问过，就直接返回
    if file_path in visited:
        return

    # 注意：要先把它加入 visited，才能避免环形链接重复扫描
    visited.add(file_path)

    # 检查节点本身
    filename, issues = check_node_file(file_path)
    if issues:
        empty_nodes[filename] = issues

    # 提取本文件的所有链接
    existing_links, missing_links = extract_local_html_links(file_path)

    # 对于链接到不存在文件的情况，记为问题
    for href, link_text in missing_links:
        add_issue_to_empty_nodes(
            filename,
            f"链接到不存在的文件: {href}（链接文字: \"{link_text}\"）"
        )

    # 继续解析存在的子链接
    for link in existing_links:
        dfs_scan(link)

# ========== 主逻辑 ==========

def main():
    # 1. 先从项目根目录下的 index.html 开始扫描
    root_path = os.path.abspath(ROOT_HTML)
    if os.path.isfile(root_path):
        dfs_scan(root_path)
    else:
        print(f"警告：根文件 {ROOT_HTML} 不存在，无法从 index.html 递归扫描。")

    # 2. 如果还有其余 .html 是"孤立的"，也要检查
    all_htmls = list(Path(".").rglob("*.html"))
    for html_file in all_htmls:
        abs_file = os.path.abspath(html_file)
        if abs_file not in visited:
            # 说明该文件没被任何已扫描节点链接到，也要单独检查一下
            dfs_scan(abs_file)

    # 3. 将结果写入输出文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        if empty_nodes:
            out_file.write(f"扫描完成，发现 {len(empty_nodes)} 个文件存在问题：\n\n")
            for fname, issues in empty_nodes.items():
                out_file.write(f"文件: {fname}\n")
                for issue in issues:
                    out_file.write(f"  - {issue}\n")
                out_file.write("\n")
        else:
            out_file.write("扫描完成，未发现空节点、缺失区域或无效链接。\n")

    print("扫描完成，结果已写入:", OUTPUT_FILE)

if __name__ == "__main__":
    main()