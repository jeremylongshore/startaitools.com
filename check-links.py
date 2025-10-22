#!/usr/bin/env python3
"""
Link checker for startaitools.com
Tests all HTTP/HTTPS links in markdown files
"""

import re
import sys
import subprocess
from pathlib import Path
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_urls_from_file(file_path):
    """Extract all HTTP/HTTPS URLs from a markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all HTTP/HTTPS URLs - only ASCII characters
    urls = re.findall(r'https?://[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=]+', content)
    # Clean up trailing punctuation
    cleaned = []
    for url in urls:
        url = url.rstrip(').,;:!?\'"`')
        # Remove any trailing backticks or quotes
        url = url.rstrip('`"\'')
        cleaned.append((url, file_path))
    return cleaned

def is_external_url(url):
    """Check if URL is external (not localhost, not schema definitions)"""
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False
        if parsed.hostname in ['localhost', '127.0.0.1', 'json-schema.org']:
            return False
        if 'localhost:' in url or '127.0.0.1:' in url:
            return False
        return True
    except Exception:
        return False

def test_url(url):
    """Test if URL is accessible using curl"""
    try:
        # Use curl with timeout and follow redirects
        result = subprocess.run(
            ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '-L', '--max-time', '10', url],
            capture_output=True,
            text=True,
            timeout=15
        )
        status_code = result.stdout.strip()
        return int(status_code) if status_code.isdigit() else 0
    except Exception as e:
        return 0

def main():
    # Find all markdown files
    content_dir = Path('content')
    md_files = list(content_dir.rglob('*.md'))

    print(f"Scanning {len(md_files)} markdown files...")

    # Extract all URLs
    all_urls = {}
    for md_file in md_files:
        urls = extract_urls_from_file(md_file)
        for url, file_path in urls:
            if is_external_url(url):
                if url not in all_urls:
                    all_urls[url] = []
                all_urls[url].append(str(file_path))

    print(f"Found {len(all_urls)} unique external URLs to test")

    # Test URLs in parallel
    broken_links = []
    working_links = []

    print("\nTesting URLs (this may take a while)...")

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(test_url, url): url for url in all_urls.keys()}

        for i, future in enumerate(as_completed(future_to_url), 1):
            url = future_to_url[future]
            try:
                status_code = future.result()

                if status_code == 0 or status_code >= 400:
                    broken_links.append((url, status_code, all_urls[url]))
                    print(f"[{i}/{len(all_urls)}] ❌ {status_code} - {url}")
                else:
                    working_links.append((url, status_code))
                    if i % 50 == 0:
                        print(f"[{i}/{len(all_urls)}] Tested {i} URLs...")
            except Exception as e:
                broken_links.append((url, 0, all_urls[url]))
                print(f"[{i}/{len(all_urls)}] ❌ ERROR - {url}")

    # Report results
    print("\n" + "="*80)
    print("LINK CHECK REPORT")
    print("="*80)
    print(f"\nTotal URLs tested: {len(all_urls)}")
    print(f"Working links: {len(working_links)}")
    print(f"Broken links: {len(broken_links)}")

    if broken_links:
        print("\n" + "="*80)
        print("BROKEN LINKS:")
        print("="*80)
        for url, status, files in broken_links:
            print(f"\n❌ {url}")
            print(f"   Status: {status if status else 'TIMEOUT/ERROR'}")
            print(f"   Found in:")
            for file in files:
                print(f"   - {file}")

    # Write report to file
    with open('link-check-report.txt', 'w') as f:
        f.write("LINK CHECK REPORT\n")
        f.write("="*80 + "\n\n")
        f.write(f"Total URLs tested: {len(all_urls)}\n")
        f.write(f"Working links: {len(working_links)}\n")
        f.write(f"Broken links: {len(broken_links)}\n\n")

        if broken_links:
            f.write("="*80 + "\n")
            f.write("BROKEN LINKS:\n")
            f.write("="*80 + "\n")
            for url, status, files in broken_links:
                f.write(f"\n❌ {url}\n")
                f.write(f"   Status: {status if status else 'TIMEOUT/ERROR'}\n")
                f.write(f"   Found in:\n")
                for file in files:
                    f.write(f"   - {file}\n")

    print(f"\nDetailed report saved to: link-check-report.txt")

    return 0 if not broken_links else 1

if __name__ == '__main__':
    sys.exit(main())
