#!/usr/bin/env python3
"""
Cleanup script for NPC Advisory Opinions 2018-035 through 2018-045.
Rebuilds markdown files with proper structure per skill requirements.
"""
import os
import re
from datetime import datetime

base_path = "/sessions/keen-intelligent-newton/mnt/NPC_issuances/content/advisory-opinions/2018"

# Define cleanup specifications for each file
files_config = {
    "advisory-opinion-no-2018-037-npc-advisory-opinion-no-2018-037.md": {
        "title": "NPC Advisory Opinion No. 2018-037",
        "description": "Data Privacy Act applies to archives and libraries processing personal information, including historical research and deceased individuals."
    },
    "advisory-opinion-no-2018-038-npc-advisory-opinion-no-2018-038.md": {
        "title": "NPC Advisory Opinion No. 2018-038",
        "description": "DOTr is the personal information controller for processing of Concessionary beep cards through AF Payments Inc. as processor."
    },
    "advisory-opinion-no-2018-039-npc-advisory-opinion-no-2018-039.md": {
        "title": "NPC Advisory Opinion No. 2018-039",
        "description": "Employees may request deletion of personal data if conditions are met, subject to legal retention requirements."
    },
    "advisory-opinion-no-2018-040-npc-advisory-opinion-no-2018-040.md": {
        "title": "NPC Advisory Opinion No. 2018-040",
        "description": "BSP may publish names of sanctioned directors and officers as part of regulatory mandate, subject to proportionality principle."
    },
    "advisory-opinion-no-2018-041-npc-advisory-opinion-no-2018-041.md": {
        "title": "NPC Advisory Opinion No. 2018-041",
        "description": "Employee consent not required to submit personal information under Pasig City Ordinance, but transparency notice required."
    },
    "advisory-opinion-no-2018-042-npc-advisory-opinion-no-2018-042.md": {
        "title": "NPC Advisory Opinion No. 2018-042",
        "description": "Employees have right to access employment records, subject to confidentiality and data protection principles."
    },
    "advisory-opinion-no-2018-043-npc-advisory-opinion-no-2018-043.md": {
        "title": "NPC Advisory Opinion No. 2018-043",
        "description": "Microsoft Office 365 is a data processing system; registration required only if processing 1,000+ individuals in Philippines."
    },
    "advisory-opinion-no-2018-044-npc-advisory-opinion-no-2018-044.md": {
        "title": "NPC Advisory Opinion No. 2018-044",
        "description": "Hospital disclosure of diagnostic test information requires consent or legal authorization; patient confidentiality applies."
    },
    "advisory-opinion-no-2018-045-npc-advisory-opinion-no-2018-045.md": {
        "title": "NPC Advisory Opinion No. 2018-045",
        "description": "Patients have right to access clinical information; DOH rule on telephone inquiries does not restrict general access requests."
    }
}

# Update frontmatter in each file
for filename, config in files_config.items():
    filepath = os.path.join(base_path, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace frontmatter
        new_frontmatter = f"""---
title: "{config['title']}"
description: "{config['description']}"
tags:
  - issuance
  - type/advisory-opinion
  - year/2018
draft: false
---"""

        # Find and replace frontmatter section
        match = re.match(r'^---\n.*?\n---\n', content, re.DOTALL)
        if match:
            content = new_frontmatter + content[match.end():]

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"Updated frontmatter: {filename}")

print("Cleanup script completed")
