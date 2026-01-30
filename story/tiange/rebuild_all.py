
import os
import re

directory = r'c:\jli\projects\PublicMaterial\story\tiange'

def get_chapter_number(filename):
    if filename == 'prologue.md':
        return 0
    match = re.search(r'chapter_(\d+)', filename)
    return int(match.group(1)) if match else float('inf')

# Get all chapter files
files = [f for f in os.listdir(directory) if f == 'prologue.md' or (f.startswith('chapter_') and f.endswith('.md'))]
files.sort(key=get_chapter_number)

# 1. Update Navigation Badges
print("Updating navigation badges...")
for i, filename in enumerate(files):
    filepath = os.path.join(directory, filename)
    
    prev_file = files[i-1] if i > 0 else None
    next_file = files[i+1] if i < len(files) - 1 else None
    
    nav_links = []
    nav_links.append(f"[Start](index.md)")
    if prev_file:
        nav_links.append(f"[Previous]({prev_file})")
    if next_file:
        nav_links.append(f"[Next]({next_file})")
        
    nav_line = " | ".join(nav_links) + "\n\n"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Remove existing nav line if it starts with [Start]
        if lines and lines[0].strip().startswith("[Start](index.md)"):
            lines = lines[1:]
            # Remove any trailing empty lines after the old nav badge
            while lines and not lines[0].strip():
                lines = lines[1:]

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(nav_line + "".join(lines))
        # print(f"Updated badges for {filename}")
    except Exception as e:
        print(f"Error processing badges for {filename}: {e}")

# 2. Rebuild index.md
print("Rebuilding index.md...")
index_path = os.path.join(directory, 'index.md')
index_lines = ["# 天歌 (Tiange) - 目录\n", "\n", "## 正文\n", "\n", "- [楔子：岁时](prologue.md)\n"]

for filename in files:
    if filename == 'prologue.md':
        continue
    filepath = os.path.join(directory, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Skip the first line which is the nav badge we just added
            f.readline() 
            # Skip empty lines
            title_line = ""
            while not title_line.strip():
                title_line = f.readline()
                if not title_line: break
            
            title = title_line.lstrip('#').strip()
            index_lines.append(f"- [{title}]({filename})\n")
    except Exception as e:
        print(f"Error reading title for {filename}: {e}")

with open(index_path, 'w', encoding='utf-8') as f:
    f.writelines(index_lines)

print("Done.")
