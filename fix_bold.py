import os
import re

files = ["Chapter_01.md", "Chapter_02.md", "Chapter_03.md", "Chapter_04.md", "Chapter_05.md"]

for filename in files:
    if not os.path.exists(filename):
        continue
    
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Move ** inside the full-width parentheses with a space
    content = content.replace("**（", "（ **")
    content = content.replace("）**", "** ）")
    
    # 2. Move ** inside the curly braces with a space
    content = content.replace("{**", "{ **")
    content = content.replace("**}", "** }")
    
    # 3. Handle ** glued to CJK characters by ensuring a space outside
    # If a ** pair is tightly preceded or followed by non-space, add a space outside
    # E.g. 历史（れきし）**について**調べて -> 历史（れきし） **について** 調べて
    # We match **...** and replace it with space around it, then strip excessive spaces later if needed.
    # To be safe, let's just replace `**` that touches Japanese characters with ` ** ` or ` **`
    
    def add_spaces(match):
        text = match.group(0)
        # We want to return ` **text** `
        return f" **{match.group(1)}** "
        
    content = re.sub(r'(?<=[^\s])\*\*(.*?)\*\*(?=[^\s])', add_spaces, content)
    
    # Clean up any double spaces we might have created
    content = content.replace("  **", " **")
    content = content.replace("**  ", "** ")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

print("Formatting fixed!")
