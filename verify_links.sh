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
    "/posts/%C3%BC%C3%B6%C3%A4-the-complete-ai-engineering-curriculum-from-zero-to-200k-salary/"
    "/posts/scaling-ai-inference-to-billions-of-users-and-agents-google-clouds-decade-long-journey/"
)

for link in "${links[@]}"; do
    # Convert URL-encoded path to filesystem path
    fs_path=$(echo "$link" | sed 's|^/||; s|%C3%BC|ü|g; s|%C3%B6|ö|g; s|%C3%A4|ä|g')
    full_path="public/${fs_path}index.html"
    
    if [ -f "$full_path" ]; then
        echo "✅ EXISTS: $link"
    else
        echo "❌ MISSING: $link (looked for: $full_path)"
    fi
done
