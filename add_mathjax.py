#!/usr/local/bin/python3
import os
import re

# 1) 先统一将 src="js/mathjax-config.js" 改成 src="../js/mathjax-config.js"
rewrite_config_path_pattern = re.compile(
    r'(src=")js/mathjax-config\.js(")',
    re.IGNORECASE
)

# 2) 用来匹配 config 脚本 (现在只需要匹配 ../js/mathjax-config.js)
config_script_pattern = re.compile(
    r'<script[^>]*src="\.\./js/mathjax-config\.js"[^>]*>.*?</script>',
    re.IGNORECASE | re.DOTALL
)

# 3) 用来匹配 MathJax 主脚本 (id="MathJax-script")
mathjax_script_pattern = re.compile(
    r'<script[^>]*id="MathJax-script"[^>]*>.*?</script>',
    re.IGNORECASE | re.DOTALL
)

# Walk through all HTML files in the project
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # ========== 第一步：强制将 script src="js/mathjax-config.js" 改成 "../js/mathjax-config.js" ==========
            # 注意：若已是 ../js/ 则不变；若是 /js/，则会被替换成 ../js/。
            content_rewritten = rewrite_config_path_pattern.sub(r'\1../js/mathjax-config.js\2', content)
            
            # ========== 第二步：查找并重排顺序（仅当二者都存在时） ==========
            found_config = config_script_pattern.search(content_rewritten)
            found_mathjax = mathjax_script_pattern.search(content_rewritten)
            
            if found_config and found_mathjax:
                # 移除这两个脚本标签
                without_scripts = config_script_pattern.sub('', content_rewritten)
                without_scripts = mathjax_script_pattern.sub('', without_scripts)
                
                # 生成新的插入片段：config脚本在前，MathJax脚本在后
                insertion = found_config.group(0) + "\n" + found_mathjax.group(0)
                
                # 在 </head> 前插入
                new_content = re.sub(
                    r'</head>',
                    insertion + "\n</head>",
                    without_scripts,
                    count=1,
                    flags=re.IGNORECASE
                )
            else:
                # 若找不到两者，则只使用改完路径的内容
                new_content = content_rewritten
            
            # 如果内容有变化，则写回
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {file_path}")
            else:
                print(f"No change needed for {file_path}")
