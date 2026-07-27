#!/bin/bash
# Verify key links exist in public/

echo "=== Verifying Links from research.md ==="
echo ""

# Check each key link
links=(
    "/research/nlweb-conversational-interfaces/"
    "/tiny-recursive-models/"
    "/mcp-for-beginners/"
    "/posts/hybrid-ai-stack-reduce-ai-api-costs-by-60-80-with-intelligent-request-routing/"
    "/posts/the-complete-ai-engineering-curriculum-from-zero-to-200k-salary/"
)

for link in "${links[@]}"; do
    full_path="public${link}index.html"

    if [ -f "$full_path" ]; then
        echo "✅ EXISTS: $link"
    else
        echo "❌ MISSING: $link (looked for: $full_path)"
    fi
done

echo ""
echo "Removed 2026-07-27:"
echo "  - /posts/scaling-ai-inference-to-billions-...  (no such post on this site; removed"
echo "    from content/posts/research-curriculum.md)"
echo "  - /posts/\%C3\%BC\%C3\%B6\%C3\%A4-...the-complete-ai-engineering-curriculum-..."
echo "    (URL-encoded slugs don't match Hugo's render — Hugo serves the file as"
echo "    /posts/the-complete-ai-engineering-curriculum-from-zero-to-200k-salary/ which"
echo "    is what the curriculum link now points at)"
