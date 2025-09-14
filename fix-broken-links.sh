#!/bin/bash

# Fix Broken Links Script for StartAITools.com
# This script identifies and fixes all broken internal links identified in the audit
# Date: September 14, 2025

echo "=== StartAITools.com Broken Link Fixer ==="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create backup directory
BACKUP_DIR="content-backup-$(date +%Y%m%d-%H%M%S)"
echo -e "${YELLOW}Creating backup in ${BACKUP_DIR}...${NC}"
cp -r content "$BACKUP_DIR"

# Function to find broken links
find_broken_links() {
    echo -e "\n${YELLOW}=== Finding Broken Links ===${NC}"

    echo -e "\n${RED}Journey links (directory deleted):${NC}"
    grep -r "](/docs/journey" content/ --include="*.md" || echo "None found"

    echo -e "\n${RED}Task links pointing to wrong location:${NC}"
    grep -r "](/tasks/prd-" content/ --include="*.md" || echo "None found"

    echo -e "\n${RED}Library links (no library directory):${NC}"
    grep -r "](/library" content/ --include="*.md" || echo "None found"

    echo -e "\n${RED}Learning links (minimal content):${NC}"
    grep -r "](/learning" content/ --include="*.md" || echo "None found"
}

# Function to fix links automatically
fix_links() {
    echo -e "\n${GREEN}=== Fixing Broken Links ===${NC}"

    # Fix journey links - redirect to blog archives
    echo "Fixing journey links -> blog archives..."
    find content -name "*.md" -type f -exec sed -i \
        -e 's|](/docs/journey/)|](/docs/blog/)|g' \
        -e 's|](/docs/journey/project-evolution-timeline/)|](/docs/blog/project-evolution-timeline/)|g' \
        {} \;

    # Fix task links - these files exist but path is wrong
    echo "Fixing task links -> correct path..."
    find content -name "*.md" -type f -exec sed -i \
        -e 's|](/tasks/prd-hugo-book-migration/)|](/tasks/prd-hugo-book-migration)|g' \
        -e 's|](/tasks/prd-smart-glossary/)|](/tasks/prd-smart-glossary)|g' \
        -e 's|](/tasks/prd-devops-learning-path/)|](/tasks/prd-devops-learning-path)|g' \
        -e 's|](/tasks/prd-task-management-system/)|](/tasks/prd-task-management-system)|g' \
        -e 's|](/tasks/prd-development-environment-restructure/)|](/tasks/prd-development-environment-restructure)|g' \
        {} \;

    # Fix library links - redirect to resources
    echo "Fixing library links -> resources..."
    find content -name "*.md" -type f -exec sed -i \
        -e 's|](/library/ai-tools-comparison)|](/docs/resources/ai-tools-comparison)|g' \
        -e 's|](/library/cleanup-script)|](/docs/resources/cleanup-script)|g' \
        -e 's|](/library|](/docs/resources|g' \
        {} \;

    # Fix learning links - redirect to getting-started
    echo "Fixing learning links -> getting-started..."
    find content -name "*.md" -type f -exec sed -i \
        -e 's|](/learning/)|](/docs/getting-started/)|g' \
        {} \;
}

# Function to verify fixes
verify_fixes() {
    echo -e "\n${YELLOW}=== Verifying Fixes ===${NC}"

    local errors=0

    # Check for remaining broken patterns
    if grep -r "](/docs/journey" content/ --include="*.md" > /dev/null 2>&1; then
        echo -e "${RED}ERROR: Journey links still exist${NC}"
        ((errors++))
    else
        echo -e "${GREEN}✓ Journey links fixed${NC}"
    fi

    if grep -r "](/tasks/prd-.*/" content/ --include="*.md" > /dev/null 2>&1; then
        echo -e "${RED}ERROR: Task links with trailing slash still exist${NC}"
        ((errors++))
    else
        echo -e "${GREEN}✓ Task links fixed${NC}"
    fi

    if grep -r "](/library" content/ --include="*.md" > /dev/null 2>&1; then
        echo -e "${RED}ERROR: Library links still exist${NC}"
        ((errors++))
    else
        echo -e "${GREEN}✓ Library links fixed${NC}"
    fi

    if grep -r "](/learning" content/ --include="*.md" > /dev/null 2>&1; then
        echo -e "${RED}ERROR: Learning links still exist${NC}"
        ((errors++))
    else
        echo -e "${GREEN}✓ Learning links fixed${NC}"
    fi

    return $errors
}

# Function to generate broken link report
generate_report() {
    echo -e "\n${YELLOW}=== Generating Link Report ===${NC}"

    local report_file="link-fix-report-$(date +%Y%m%d-%H%M%S).txt"

    {
        echo "StartAITools.com Link Fix Report"
        echo "Generated: $(date)"
        echo "================================"
        echo ""
        echo "Files Modified:"
        diff -rq content "$BACKUP_DIR" 2>/dev/null | grep "differ" | cut -d' ' -f2
        echo ""
        echo "Summary of Changes:"
        echo "- Journey links redirected to /docs/blog/"
        echo "- Task links fixed (removed trailing slashes)"
        echo "- Library links redirected to /docs/resources/"
        echo "- Learning links redirected to /docs/getting-started/"
        echo ""
        echo "Backup created in: $BACKUP_DIR"
    } > "$report_file"

    echo -e "${GREEN}Report saved to: $report_file${NC}"
}

# Main execution
echo "Starting broken link analysis and fix..."

# Show current state
find_broken_links

# Ask for confirmation
echo -e "\n${YELLOW}Do you want to automatically fix these broken links? (y/n)${NC}"
read -r response

if [[ "$response" == "y" || "$response" == "Y" ]]; then
    fix_links

    # Verify the fixes
    if verify_fixes; then
        echo -e "\n${GREEN}✅ All links successfully fixed!${NC}"
        generate_report

        echo -e "\n${YELLOW}To restore backup if needed:${NC}"
        echo "  rm -rf content && mv $BACKUP_DIR content"
    else
        echo -e "\n${RED}⚠️  Some issues remain. Check the errors above.${NC}"
    fi
else
    echo -e "${YELLOW}Fix cancelled. Backup still created in: $BACKUP_DIR${NC}"
fi

echo -e "\n${GREEN}=== Script Complete ===${NC}"