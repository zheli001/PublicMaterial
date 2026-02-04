import os
import re

# Base path
base_path = r"c:\jli\projects\PublicMaterial\story\laset_rejection"
tmp_path = r"c:\jli\projects\PublicMaterial\tmp\laset_rejection"

# Map of filename to new Title text (Aesthetic Sinking Theme)
title_map = {
    "prologue.md":   ("序章", "蓝调晨曦"),         # Blue Dawn (Hypnosis)
    "chapter_01.md": ("第一章", "流动的琥珀"),       # Flowing Amber (Trapped in flow)
    "chapter_02.md": ("第二章", "天鹅绒知识"),       # Velvet Knowledge (Soft suffocation)
    "chapter_03.md": ("第三章", "镜面舞步"),         # Mirror Dance (Narcissistic connection)
    "chapter_04.md": ("第四章", "深海回响"),         # Deep Sea Echo (The log)
    "chapter_05.md": ("第五章", "偏离的音符"),       # Deviating Note (Social awkwardness)
    "chapter_06.md": ("第六章", "颤抖的琴弦"),       # Trembling Strings (Anxiety of choice)
    "chapter_07.md": ("第七章", "砂砾的质感"),       # Texture of Grit (Noodle/Realism)
    "chapter_08.md": ("第八章", "玻璃花园"),         # Glass Garden (Polite isolation)
    "chapter_09.md": ("第九章", "断线的风筝"),       # Kite Unbound (Dangerous freedom)
    "chapter_10.md": ("第十章", "微凉的裂纹"),       # Cool Cracks (Spread of anxiety)
    "chapter_11.md": ("第十一章", "荒原的微光"),      # Glimmer in Wasteland (Connection)
    "chapter_12.md": ("第十二章", "雨中的咏叹"),      # Aria in Rain (Suffering as art)
    "chapter_13.md": ("第十三章", "失语的合唱"),      # Aphasic Chorus (Loss of language)
    "chapter_14.md": ("第十四章", "水晶囚笼"),        # Crystal Cage (Observed)
    "chapter_15.md": ("第十五章", "光影替身"),        # Shadow Double (AI taking over)
    "chapter_16.md": ("第十六章", "云端的垂怜"),      # Mercy from Clouds (Condescension)
    "chapter_17.md": ("第十七章", "冬眠的决心"),      # Resolve to Hibernate (Locking in)
    "chapter_18.md": ("第十八章", "园艺的艺术"),      # Art of Gardening (Pruning/Optimization)
    "chapter_19.md": ("第十九章", "静默的退潮"),      # Silent Ebb (Giving up)
    "chapter_20.md": ("第二十章", "血色的珊瑚"),      # Blood Coral (Painful beauty)
    "chapter_21.md": ("第二十一章", "甜蜜的药丸"),     # Sweet Pill (Compromise)
    "chapter_22.md": ("第二十二章", "最后的火柴"),     # The Last Match (Dying of cold)
    "chapter_23.md": ("第二十三章", "纯白庆典"),       # Pure White Celebration (Wedding)
    "chapter_24.md": ("第二十四章", "永恒的泡沫"),     # Eternal Bubble (The ending)
}

# 1. Update Index.md
index_path = os.path.join(base_path, "index.md")
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

for filename, (prefix, title) in title_map.items():
    # Regex to replace link text: [Anything](filename) -> [Prefix｜Title](filename)
    pattern = re.compile(rf"\[.*?\]\({re.escape(filename)}\)")
    new_link = f"[{prefix}｜{title}]({filename})"
    content = pattern.sub(new_link, content)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.md")

# 2. Update Score.md
score_path = os.path.join(tmp_path, "score.md")
if os.path.exists(score_path):
    with open(score_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for filename, (prefix, title) in title_map.items():
        # Match `| **Prefix:**<br>OldTitle |` and update Title
        pattern = re.compile(rf"(\*{re.escape(prefix)}:\*\*<br>)([^|]+)")
        content = pattern.sub(rf"\1{title} ", content) 

    with open(score_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated score.md")

# 3. Update Chapter Files (Header & Nav Links)
for filename, (prefix, title) in title_map.items():
    file_path = os.path.join(base_path, filename)
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # A. Update H1
    new_h1 = f"# {prefix}｜{title}"
    content = re.sub(r"^# .*?$", new_h1, content, count=1, flags=re.MULTILINE)
    
    # B. Update Links to other chapters
    for target_file, (target_prefix, target_title) in title_map.items():
        if target_file == filename: continue
        
        def link_replacer(match):
            text = match.group(1)
            link_prefix = ""
            if "上一章" in text: link_prefix = "上一章："
            elif "下一章" in text: link_prefix = "下一章："
            elif "目录" in text: return match.group(0)
            
            if link_prefix:
                return f"[{link_prefix}{target_prefix}｜{target_title}]({target_file})"
            else:
                return f"[{target_prefix}｜{target_title}]({target_file})"

        pattern = re.compile(rf"\[([^\]]*?)\]\({re.escape(target_file)}\)")
        content = pattern.sub(link_replacer, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filename}")

print("Done.")
