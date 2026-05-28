import os
import re

files = [f"Chapter_{i:02d}.md" for i in range(1, 6)]

for filename in files:
    if not os.path.exists(filename):
        continue
        
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 1. Fix broken furigana bolding: 歴史（れきし ** ）について** -> 歴史（れきし） **について**
    # This matches `（` + no stars/parens + ` ** ）` + no stars + `**`
    content = re.sub(r'（([^\*）]+?)\s*\*\*\s*）([^\*]+?)\*\*', r'（\1） **\2**', content)
    
    # 2. Fix broken meaning lines: **【意味】〜（……** ） -> **【意味】〜（……）**
    # This matches **【意味】...** ） at the end of a line or just generally matching the line
    content = re.sub(r'(\*\*【意味】[^\n\*]+?)\s*\*\*\s*）', r'\1）**', content)
    
    # 3. Any other lines starting with ** and ending with ** ）
    content = re.sub(r'(^\*\*.*?[^\*\s])\s*\*\*\s*）$', r'\1）**', content, flags=re.MULTILINE)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

print("Parenthesis bolding fixed!")
