import os

base_dir = r"C:\Users\Bosho\Desktop\Bosho OS\General\Projects\vlm_grounding_aaai"

ordered_replacements = [
    ("â€”", "—"),
    ("âœ…", "✅"),
    ("â€™", "'"),
    ("â€œ", "“"),
    ("â€", "”")
]

for root, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".md"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            for old, new in ordered_replacements:
                content = content.replace(old, new)
                
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed encoding in {file}")
