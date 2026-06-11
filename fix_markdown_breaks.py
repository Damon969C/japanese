import glob
import re

for filename in glob.glob("Chapter_*.md"):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Add a blank line before any line starting with ①②③④⑤⑥⑦⑧⑨⑩ if there isn't one already
    content = re.sub(r'([^\n])\n([①②③④⑤⑥⑦⑧⑨⑩])', r'\1\n\n\2', content)
    
    # Also for exercises, if a line starts with a number, and the previous line was a translation
    content = re.sub(r'(- \*\*中文翻译\*\*.*?)\n(\d+\.)', r'\1\n\n\2', content)

    # Let's also do it for 'a. ', 'b. ' etc if they follow a translation (though unlikely)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
print("Fixed line breaks!")
