import os
import re

files = [f"Chapter_{i:02d}.md" for i in range(1, 6)]

for filename in files:
    if not os.path.exists(filename):
        continue
        
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Ensure a blank line before any line starting with ①-⑩ or a number like 1., 2. etc
    content = re.sub(r'(?<!\n)\n([①②③④⑤⑥⑦⑧⑨⑩])', r'\n\n\1', content)
    content = re.sub(r'(?<!\n)\n([0-9]+\.)', r'\n\n\1', content)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

print("Spacing fixed!")
