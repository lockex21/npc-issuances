#!/bin/bash

# Process all issuance markdown files
base="/sessions/awesome-festive-noether/mnt/NPC_issuances"
cd "$base"

# Create initial cleanup log if missing
if [ ! -f ".cleanup-log.md" ]; then
    echo "# NPC Issuances Cleanup Log" > .cleanup-log.md
    echo "" >> .cleanup-log.md
fi

# Generate list of files to process
for year_dir in content/issuances/{1988,2017,2020,2021,2022,2023,2024,2025}; do
    [ -d "$year_dir" ] || continue
    
    # Ensure state file exists
    state_file="$year_dir/.cleanup-state.json"
    if [ ! -f "$state_file" ]; then
        echo '{"files": {}}' > "$state_file"
    fi
    
    # List all .md files except index.md
    find "$year_dir" -maxdepth 1 -name "*.md" ! -name "index.md" -type f | sort
done
