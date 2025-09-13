#!/bin/bash

# Sync content from Start AI Tools to Jeremy Longshore blog
# This script copies select posts from Start AI Tools to the main blog

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔄 Syncing content from Start AI Tools...${NC}"

# Define paths
STARTAI_PATH="../startaitools/content/posts"
JEREMY_PATH="content/en/blogs/startai"
CURRENT_DIR=$(pwd)

# Check if we're in the right directory
if [[ ! -f "hugo.toml" ]]; then
    echo -e "${RED}❌ Error: Not in Hugo site root. Please run from jeremylongshore directory.${NC}"
    exit 1
fi

# Check if Start AI Tools directory exists
if [[ ! -d "$STARTAI_PATH" ]]; then
    echo -e "${YELLOW}⚠️  Start AI Tools content not found at $STARTAI_PATH${NC}"
    echo "Make sure both blogs are in the same parent directory."
    exit 1
fi

# Create target directory if it doesn't exist
mkdir -p "$JEREMY_PATH"

echo -e "${GREEN}📁 Created/verified directory: $JEREMY_PATH${NC}"

# Function to process front matter
process_frontmatter() {
    local file=$1
    local output=$2

    # Add a note that this is syndicated content
    sed '1,/+++/{
        /+++/a\
# Originally published on Start AI Tools\
canonical = "https://startaitools.com"
    }' "$file" > "$output"
}

# Sync specific posts (you can customize this list)
POSTS_TO_SYNC=(
    "ai-engineering-curriculum-complete.md"
    "modern-multi-agent-architecture-blueprint.md"
    "diagnostic-ai-platform-feature-preview.md"
    "building-worlds-first-universal-ai-diagnostic-platform.md"
)

echo -e "${GREEN}📝 Syncing selected posts...${NC}"

synced_count=0
for post in "${POSTS_TO_SYNC[@]}"; do
    if [[ -f "$STARTAI_PATH/$post" ]]; then
        # Create filename with startai prefix
        new_filename="startai-${post}"

        # Copy and process the file
        cp "$STARTAI_PATH/$post" "$JEREMY_PATH/$new_filename"

        # Add canonical URL and attribution
        temp_file=$(mktemp)
        {
            # Read the original file and modify front matter
            awk '
                /^+++$/ {
                    if (NR == 1) {
                        print
                        in_frontmatter = 1
                    } else if (in_frontmatter) {
                        print "canonical = \"https://startaitools.com\""
                        print "series = [\"Start AI Tools\"]"
                        print
                        in_frontmatter = 0
                    } else {
                        print
                    }
                    next
                }
                { print }
            ' "$JEREMY_PATH/$new_filename"
        } > "$temp_file"

        mv "$temp_file" "$JEREMY_PATH/$new_filename"

        echo -e "  ✅ Synced: ${post} -> ${new_filename}"
        ((synced_count++))
    else
        echo -e "  ${YELLOW}⚠️  Not found: ${post}${NC}"
    fi
done

echo -e "${GREEN}✨ Sync complete! ${synced_count} posts synced.${NC}"

# Optional: Copy images if they exist
if [[ -d "../startaitools/static/images" ]] && [[ -d "static/images" ]]; then
    echo -e "${GREEN}🖼️  Syncing images...${NC}"
    rsync -av --ignore-existing ../startaitools/static/images/ static/images/startai/
    echo -e "${GREEN}✅ Images synced${NC}"
fi

echo -e "${GREEN}🎉 All done! Run 'hugo server -D' to preview the synced content.${NC}"