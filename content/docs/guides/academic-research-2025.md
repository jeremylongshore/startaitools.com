# 🎓 Ultimate Academic Research & AI Tools Guide

**Last Updated:** September 15, 2025
**Version:** 1.0
**Author:** Jeremy Longshore

---

## 📚 Table of Contents

1. [AI Tools for Academic Research](#ai-tools)
2. [Free Academic Search Engines](#search-engines)
3. [Citation Management](#citations)
4. [Paper Access Tools](#paper-access)
5. [Linux CLI Tools](#cli-tools)
6. [Quick Start Workflows](#workflows)
7. [Direct Links & Resources](#links)

---

## 🤖 AI Tools for Academic Research {#ai-tools}

### 1. Perplexity AI ⭐ BEST OVERALL
- **Link:** https://www.perplexity.ai
- **Free Tier:** Yes (5 Pro searches/day)
- **Features:** Real-time citations, academic search
- **API:** https://docs.perplexity.ai

**Quick Search Example:**
```
"quantum computing recent papers 2024 site:arxiv.org"
```

### 2. Consensus.app ⭐ BEST FOR PAPERS
- **Link:** https://consensus.app
- **Free Tier:** Yes (unlimited basic searches)
- **Database:** 200+ million papers
- **Special:** Only peer-reviewed sources

### 3. Elicit ⭐ BEST FOR LITERATURE REVIEW
- **Link:** https://elicit.org
- **Free Tier:** 5,000 words/month
- **Features:** Paper summaries, data extraction
- **Export:** CSV, BibTeX

### 4. Claude with Web Search
- **Link:** https://claude.ai
- **Cost:** $20/month Pro
- **Best For:** Writing and analysis
- **Tip:** Ask "Search for recent papers on [topic]"

### 5. ChatGPT with Scholar Plugin
- **Link:** https://chat.openai.com
- **Cost:** $20/month Plus
- **Plugin:** ScholarAI
- **Access:** Settings → Plugins → ScholarAI

### 6. SciSpace (formerly SciReader)
- **Link:** https://typeset.io
- **Free Tier:** 2 papers/month
- **Feature:** "Explain this paper" AI

---

## 🔍 Free Academic Search Engines {#search-engines}

### Primary Sources

1. **Google Scholar**
   - Link: https://scholar.google.com
   - Coverage: Everything
   - Tip: Use "filetype:pdf" for direct PDFs

2. **Semantic Scholar**
   - Link: https://www.semanticscholar.org
   - Feature: AI-powered paper recommendations
   - API: Free with registration

3. **PubMed Central**
   - Link: https://www.ncbi.nlm.nih.gov/pmc
   - Focus: Biomedical and life sciences
   - All articles: Free full-text

4. **arXiv**
   - Link: https://arxiv.org
   - Focus: Physics, Math, CS, Biology
   - Everything: Pre-print, free

5. **CORE**
   - Link: https://core.ac.uk
   - Database: 200+ million open access papers
   - API: Available

6. **BASE**
   - Link: https://www.base-search.net
   - Coverage: 300+ million documents
   - Filter: "Open Access" only

### Specialized Databases

- **SSRN** (Social Sciences): https://www.ssrn.com
- **RePEc** (Economics): https://www.repec.org
- **bioRxiv** (Biology): https://www.biorxiv.org
- **ChemRxiv** (Chemistry): https://chemrxiv.org
- **PsyArXiv** (Psychology): https://psyarxiv.com
- **DOAJ** (Open Access Journals): https://doaj.org

---

## 📝 Citation Management Tools {#citations}

### Free & Open Source

1. **Zotero** ⭐ RECOMMENDED
   - Link: https://www.zotero.org
   - Storage: 300MB free
   - Features: Browser plugin, Word/LibreOffice integration
   - Sync: Across all devices

2. **Mendeley**
   - Link: https://www.mendeley.com
   - Storage: 2GB free
   - Owner: Elsevier
   - Feature: Social networking

3. **JabRef** (Linux-friendly)
   - Link: https://www.jabref.org
   - Format: BibTeX native
   - Platform: Java-based, cross-platform

### Quick Citation Generators

- **ZoteroBib**: https://zbib.org (instant bibliography)
- **Citation Machine**: https://www.citationmachine.net
- **MyBib**: https://www.mybib.com
- **DOI to Citation**: https://doi2bib.org

---

## 🔓 Paper Access Tools {#paper-access}

### Legal & Open Access

1. **Unpaywall** (Browser Extension)
   - Link: https://unpaywall.org
   - Finds: Legal open-access versions
   - Coverage: 30+ million papers

2. **Open Access Button**
   - Link: https://openaccessbutton.org
   - Feature: Request from authors
   - Success Rate: ~50%

3. **PaperPanda**
   - Link: https://paperpanda.app
   - Feature: Finds free legal versions

4. **Google Scholar PDF Finder**
   - Tip: Click "All X versions" link
   - Often finds: University repositories

### Direct from Authors

- **ResearchGate**: https://www.researchgate.net
- **Academia.edu**: https://www.academia.edu
- **Author Email**: Most papers list email - just ask!

### Alternative Access (Use Responsibly)

- **Sci-Hub** (Controversial)
  - Current mirrors: Check https://sci-hub.se
  - Coverage: 85+ million papers
  - Legal: Varies by country

- **Library Genesis**
  - Books & papers
  - Multiple mirrors available

---

## 💻 Linux CLI Tools {#cli-tools}

### Installation & Setup

```bash
# Python tools
pip install scholarly pybliometrics arxiv-cli

# Zotero CLI
npm install -g zotero-cli

# PDF tools
sudo apt install poppler-utils pdfgrep

# Citation extraction
pip install reference-extractor
```

### Command Line Examples

```bash
# Search Google Scholar
python3 -c "
from scholarly import scholarly
search_query = scholarly.search_pubs('quantum computing 2024')
for i in range(5):
    paper = next(search_query)
    print(f\"{paper['bib']['title']} - {paper['bib'].get('pub_year', 'N/A')}\")
"

# Search arXiv
arxiv-cli search "quantum computing" --max-results 10

# Extract citations from PDF
reference-extractor paper.pdf > citations.txt

# Search inside PDFs
pdfgrep -i "methodology" *.pdf

# Download from DOI
curl -LH "Accept: application/pdf" https://doi.org/10.1234/example -o paper.pdf
```

### API Access Scripts

```bash
# Semantic Scholar API
curl -X GET "https://api.semanticscholar.org/graph/v1/paper/search?query=quantum+computing&limit=10" \
  | jq '.data[] | {title: .title, year: .year, doi: .doi}'

# Crossref API
curl "https://api.crossref.org/works?query=quantum+computing&rows=5" \
  | jq '.message.items[] | {title: .title[0], doi: .DOI}'

# arXiv API
curl "http://export.arxiv.org/api/query?search_query=quantum+computing&max_results=5"
```

---

## 📋 Quick Start Workflows {#workflows}

### Workflow 1: Quick Literature Review

1. **Start:** Consensus.app → Get key papers
2. **Expand:** Connected Papers → Find related work
3. **Access:** Unpaywall → Get PDFs
4. **Manage:** Zotero → Organize citations
5. **Write:** Claude/GPT-4 → Draft review

### Workflow 2: Comprehensive Research

```bash
# Step 1: Broad search
Perplexity: "recent advances in [topic] 2024"

# Step 2: Academic search
Google Scholar: "allintitle: [specific terms]"
Semantic Scholar: Filter by "Highly Influential"

# Step 3: Get papers
Unpaywall extension → Legal access
ResearchGate → Request from authors

# Step 4: Manage
Import to Zotero → Tag and organize

# Step 5: Analyze
Upload to Claude → "Summarize key findings"
```

### Workflow 3: CLI Power User

```bash
#!/bin/bash
# research.sh - Automated research script

TOPIC="$1"
mkdir -p "research_$TOPIC"
cd "research_$TOPIC"

# Search multiple sources
echo "Searching arXiv..."
arxiv-cli search "$TOPIC" --max-results 20 > arxiv_results.txt

echo "Searching Semantic Scholar..."
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=$TOPIC&limit=20" \
  | jq -r '.data[] | "\(.title) | \(.year) | \(.doi)"' > semantic_results.txt

echo "Results saved to research_$TOPIC/"
```

---

## 🔗 Direct Links & Resources {#links}

### Must-Have Browser Extensions

1. **Zotero Connector**: [Chrome](https://chrome.google.com/webstore/detail/zotero-connector/) | [Firefox](https://www.zotero.org/download/)
2. **Unpaywall**: [Chrome](https://chrome.google.com/webstore/detail/unpaywall/) | [Firefox](https://addons.mozilla.org/en-US/firefox/addon/unpaywall/)
3. **Google Scholar Button**: [Chrome](https://chrome.google.com/webstore/detail/google-scholar-button/)
4. **Lean Library**: [Get Extension](https://www.leanlibrary.com)

### Research Communities

- **r/Scholar**: https://reddit.com/r/Scholar (paper requests)
- **#icanhazpdf**: Twitter hashtag for paper requests
- **PubPeer**: https://pubpeer.com (post-publication peer review)

### Writing & Formatting

- **Overleaf**: https://www.overleaf.com (LaTeX editor)
- **Authorea**: https://www.authorea.com (collaborative writing)
- **Typst**: https://typst.app (modern LaTeX alternative)

### Data & Code

- **Papers with Code**: https://paperswithcode.com
- **GitHub Scholar**: Search GitHub for academic code
- **Zenodo**: https://zenodo.org (research data repository)
- **OSF**: https://osf.io (Open Science Framework)

---

## 💡 Pro Tips

### Google Scholar Advanced

```
# Exact phrase
"quantum entanglement"

# Exclude terms
quantum -classical

# Date range
quantum computing after:2023

# Author search
author:"Feynman"

# Title only
allintitle: quantum computing

# Combine
allintitle: quantum computing after:2023 -review
```

### API Keys (Free Tier)

- **Semantic Scholar**: Register at https://www.semanticscholar.org/product/api
- **CORE**: Register at https://core.ac.uk/services/api
- **Crossref**: No key needed, be polite with requests
- **arXiv**: No key needed, respect rate limits

### Citation Formats

```bash
# Convert citations
pandoc --citeproc --bibliography=refs.bib -t markdown paper.md -o paper_cited.md

# Extract DOIs from PDF
pdftotext paper.pdf - | grep -oP '10\.\d{4,}/[-._;()/:\w]+' | sort -u
```

---

## 🆘 Troubleshooting

**Can't access a paper?**
1. Try Google Scholar "All versions"
2. Check ResearchGate
3. Email the author
4. Try your library's proxy
5. Check preprint servers

**Too many results?**
- Add year filters
- Use "review" or "survey" keywords
- Sort by citations/relevance
- Use advanced search operators

**Need older papers?**
- **JSTOR**: https://www.jstor.org (some free access)
- **Internet Archive**: https://archive.org/details/texts
- **HathiTrust**: https://www.hathitrust.org

---

## 📅 Updates & Maintenance

This guide is current as of **January 15, 2025**.

For updates:
- Check tool websites for API changes
- Sci-Hub mirrors change frequently
- New AI tools emerge monthly

---

## 📜 License & Sharing

This guide is free to share and modify. Created by Jeremy Longshore with AI assistance.

**Share this guide:** Save as PDF or bookmark
**Improve it:** Send suggestions or make your own version
**Stay updated:** Academic tools evolve quickly!

---

*Remember: Always respect copyright and use tools ethically. When in doubt, ask your librarian!*