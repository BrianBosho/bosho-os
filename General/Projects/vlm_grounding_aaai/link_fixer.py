import os
import re

base_dir = r"C:\Users\Bosho\Desktop\Bosho OS\General\Projects\vlm_grounding_aaai"

replacements = {
    r"\[\[vlm_grounding_aaai\]\]": "[[00_control/project_index.md|vlm_grounding_aaai]]",
    r"\[\[execution\]\]": "[[00_control/execution.md|execution]]",
    r"\[\[vlm_grounding_aaai/archive\|archive\]\]": "[[90_archive/archive_old.md|archive]]",
    r"\[\[To-Do\]\]": "[[10_paper/PAPER_EXECUTION_TODO.md|To-Do]]",
    r"\[\[Planning/To-Do\]\]": "[[10_paper/PAPER_EXECUTION_TODO.md|To-Do]]",
    r"\[\[This Week\]\]": "[[00_control/execution.md|This Week]]",
    r"\[\[Planning/This Week\]\]": "[[00_control/execution.md|This Week]]",
    r"\[\[VLM Grounding Synthesis\]\]": "[[90_archive/old_direction_notes/VLM Grounding Synthesis.md|VLM Grounding Synthesis]]",
    r"\[\[VLM Grounding Resources\]\]": "[[60_literature/resources.md|VLM Grounding Resources]]",
    r"\[\[VLM Grounding Direction\]\]": "[[90_archive/old_direction_notes/VLM Grounding Direction.md|VLM Grounding Direction]]",
    r"\[\[VLM Grounding Phase 2 Notes\]\]": "[[90_archive/old_direction_notes/VLM Grounding Phase 2 Notes.md|VLM Grounding Phase 2 Notes]]",
    r"\[\[PAPER_TRACK_FROZEN_v2\]\]": "[[10_paper/PAPER_TRACK_FROZEN_v2.md|PAPER_TRACK_FROZEN_v2]]",
}

for root, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".md"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            for old, new in replacements.items():
                content = re.sub(old, new, content)
                
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated links in {file}")
