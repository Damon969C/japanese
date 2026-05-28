import os
import re

files = [f"Chapter_{i:02d}.md" for i in range(1, 6)]

for filename in files:
    if not os.path.exists(filename):
        continue
        
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 1. Fix spaces inside bold markers
    # Pattern: ** followed by spaces, then content, then spaces, then **
    # We want to move those spaces OUTSIDE the bold markers.
    
    # We will do this carefully with a function
    def fix_bold_spaces(match):
        left_space = match.group(1)
        inner_content = match.group(2)
        right_space = match.group(3)
        return f"{left_space}**{inner_content}**{right_space}"
        
    # Find all **...** that have space(s) right inside them.
    # We match **(spaces)(content)(spaces)**
    # This regex looks for ** followed by optional spaces, content, optional spaces, **
    # where at least one of the spaces is non-empty.
    # Actually, simpler: replace `** ` with ` **` and ` **` with `** ` iteratively, but we don't want to mess up adjacent text.
    
    # Let's replace `** ` with ` **` if it's the start of the bold marker... wait, how to distinguish start/end?
    # Usually they come in pairs.
    # Let's use a non-greedy match for the whole pair:
    content = re.sub(r'\*\*([ \t]+)(.*?)([ \t]+)\*\*', r' **\2** ', content)
    content = re.sub(r'\*\*([ \t]+)(.*?)\*\*', r' **\2**', content)
    content = re.sub(r'\*\*(.*?)([ \t]+)\*\*', r'**\1** ', content)
    
    # 2. Fix the specific meaning header problem: `**【意味】〜の限度まで（到……限度为止；尽……所能） **`
    # It might have been fixed by the above, becoming `**【意味】〜の限度まで（到……限度为止；尽……所能）** `
    # Let's check for `）** ` and remove trailing space if it's just before a newline.
    
    # 3. Fix the paragraph exercises spacing explicitly:
    # （1. **e. によると** ）
    # Sometimes it might be （ **1. e. によると** ）
    # The user wanted:
    # わたしの兄（あに）は、現在（げんざい）、京都（きょうと）のある大学（だいがく）で環境（かんきょう）デザインを勉強（べんきょう）している。兄（1. e. によると ** ）、
    # Wait, the user's text was missing the first **!
    # Let's see if there are any missing `**`.
    
    # Let's just fix the `1. a. 选项` style to be tightly bolded.
    # Like `（1. **a. 选项** ）` or `（ **1. a. 选项** ）`. Let's standardise to `（ **1. a. 选项** ）`.
    # Match: `（\s*(\d+)\.\s*\*\*\s*([a-z])\.\s*([^\*]+?)\s*\*\*\s*）` -> `（ **\1. \2. \3** ）`
    # Match: `（\s*\*\*\s*(\d+)\.\s*([a-z])\.\s*([^\*]+?)\s*\*\*\s*）` -> `（ **\1. \2. \3** ）`
    # Let's just match any combination of `(`, `1.`, `a.`, `**`, and text, and reformat it.
    
    def format_exercise(match):
        num = match.group(1)
        letter = match.group(2)
        text = match.group(3).strip()
        return f"（ **{num}. {letter}. {text}** ）"
        
    # Match `（` followed by optional spaces, optional `**`, optional spaces, number, `.`, optional spaces, 
    # optional `**`, optional spaces, letter, `.`, optional spaces, optional `**`, text, optional `**`, optional spaces, `）`
    # This is getting complex. Let's just use a more targeted regex.
    # `（\s*\*?\*?\s*(\d+)\.\s*\*?\*?\s*([a-z])\.\s*\*?\*?\s*(.*?)\s*\*?\*?\s*）`
    # We want to match only inside these paragraphs.
    content = re.sub(r'（\s*(?:\*\*)?\s*(\d+)\.\s*(?:\*\*)?\s*([a-z])\.\s*(?:\*\*)?\s*([^\*）]+?)\s*(?:\*\*)?\s*）', format_exercise, content)
    
    # Let's also do the Chinese translations:
    # `（1. **a. 选项** ）` -> `（ **1. 选项** ）`
    def format_cn_exercise(match):
        num = match.group(1)
        text = match.group(2).strip()
        return f"（ **{num}. {text}** ）"
        
    content = re.sub(r'（\s*(?:\*\*)?\s*(\d+)\.\s*(?:\*\*)?\s*([^a-z\*）]+?)\s*(?:\*\*)?\s*）', format_cn_exercise, content)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

print("Bold spaces fixed!")
