#!/bin/bash

# Script to rename all files with ST6_ prefix
# Works from deepest directories first to avoid conflicts

REPO_DIR="/Users/branchechols/_Git-DL/OpenAI/openai-cookbook"
COUNTER=0
TOTAL_FILES=$(find "$REPO_DIR" -type f -not -path '*/\.*' | wc -l)

echo "Starting rename operation for approximately $TOTAL_FILES files..."
echo "================================================"

# Find all files (not directories), excluding hidden files and .git
# Sort by depth (deepest first) to avoid conflicts
find "$REPO_DIR" -type f -not -path '*/\.*' -print0 | \
while IFS= read -r -d '' file; do
    # Skip if already has ST6_ prefix
    basename=$(basename "$file")
    if [[ "$basename" == ST6_* ]]; then
        continue
    fi
    
    # Get directory and new filename
    dir=$(dirname "$file")
    newname="ST6_${basename}"
    newpath="${dir}/${newname}"
    
    # Rename the file
    if mv "$file" "$newpath" 2>/dev/null; then
        ((COUNTER++))
        # Show progress every 50 files
        if (( COUNTER % 50 == 0 )); then
            echo "Progress: $COUNTER files renamed..."
        fi
    else
        echo "ERROR: Failed to rename: $file"
    fi
done

echo "================================================"
echo "Rename operation completed!"
echo "Total files renamed: $COUNTER"