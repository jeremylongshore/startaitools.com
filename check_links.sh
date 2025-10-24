#!/bin/bash
# Comprehensive link checker for Hugo site

echo "=== Checking Internal Links on startaitools.com/research/ ==="
echo ""

# Extract all internal links from research page
curl -s https://startaitools.com/research/ | grep -oP 'href="(/[^"]+)"' | sort -u | while read -r line; do
    url=$(echo "$line" | sed 's/href="//;s/"//')
    full_url="https://startaitools.com${url}"
    
    # Check HTTP status
    status=$(curl -s -o /dev/null -w "%{http_code}" "$full_url")
    
    if [ "$status" = "404" ]; then
        echo "❌ 404 ERROR: $url"
    elif [ "$status" = "200" ]; then
        echo "✅ WORKS: $url"
    else
        echo "⚠️  STATUS $status: $url"
    fi
done
