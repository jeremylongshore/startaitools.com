# Product Requirements Document: Smart Auto-Linking Glossary

## Introduction/Overview

This PRD outlines the creation of an intelligent glossary system that automatically extracts technical terms from new content, checks against an existing glossary database, and creates bidirectional links between glossary definitions and related articles throughout the site. The system would scan uploaded content for technical terms, automatically build glossary entries, and create a knowledge graph of interconnected concepts.

## Goals

1. **Automatically extract technical terms** from any new content uploaded to the site
2. **Build a comprehensive glossary** that grows with the content
3. **Create bidirectional links** between terms and articles that reference them
4. **Detect undefined terms** and flag them for definition
5. **Connect related concepts** through intelligent cross-referencing

## User Stories

1. **As a reader**, I want to hover/click on technical terms to see quick definitions without leaving the article
2. **As Jeremy**, I want new content to automatically contribute to the glossary without manual work
3. **As a learner**, I want to see all articles that discuss a specific term when viewing its glossary entry
4. **As a content creator**, I want to be notified of undefined technical terms that need definitions

## Functional Requirements

1. **Term Extraction**
   - The system must scan new markdown files for potential technical terms
   - The system must use NLP or pattern matching to identify technical vocabulary
   - The system must check extracted terms against existing glossary
   - The system must handle variations (plural, different cases, abbreviations)

2. **Glossary Management**
   - The system must maintain a central glossary database/file
   - The system must store term, definition, aliases, and related articles
   - The system must support multiple definitions for context-dependent terms
   - The system must track first occurrence and frequency of terms

3. **Auto-Linking**
   - The system must automatically link terms in content to glossary entries
   - The system must show inline tooltips or pop-ups with definitions
   - The system must avoid over-linking (e.g., only first occurrence per section)
   - The system must handle context to link to correct definition

4. **Reverse Linking**
   - The system must maintain a list of articles using each term
   - The system must display "Used in these articles" on glossary pages
   - The system must show related terms and concepts
   - The system must update links when content changes

5. **Content Analysis**
   - The system must identify undefined technical terms
   - The system must generate reports of missing definitions
   - The system must suggest related terms based on context
   - The system must detect acronyms and attempt to expand them

## Non-Goals (Out of Scope)

1. **Will not** modify original content files (only rendered output)
2. **Will not** automatically generate definitions (only detect and link)
3. **Will not** translate or localize terms
4. **Will not** include common non-technical words

## Design Considerations

- **Performance**: Processing should happen at build time, not runtime
- **Accuracy**: Need to balance automation with accuracy (may need manual review)
- **User Experience**: Links should enhance, not clutter the reading experience
- **Maintenance**: System should be self-maintaining with minimal manual intervention

## Technical Considerations

### Implementation Approaches

1. **Build-Time Processing** (Recommended)
   ```
   1. Scan all markdown files during Hugo build
   2. Extract terms using regex or NLP library
   3. Generate glossary data file
   4. Use Hugo shortcodes to create links
   5. Build glossary pages with reverse links
   ```

2. **JavaScript Enhancement**
   - Client-side script scans content after load
   - Matches terms against glossary JSON
   - Dynamically adds links and tooltips

3. **Hybrid Approach**
   - Build-time extraction and data generation
   - Client-side enhancement for interactivity

### Technical Components

- **Term Extraction**: Python script with NLTK or spaCy
- **Data Storage**: JSON or YAML glossary file
- **Link Generation**: Hugo shortcodes or render hooks
- **UI Components**: CSS tooltips or JavaScript modals

### External Data Sources for Definitions

**Comprehensive Technical Glossaries**:
- **FOLDOC (Free On-line Dictionary of Computing)**: Searchable dictionary of computing terms, acronyms, jargon, programming languages, OS, networking
- **Tech Terms Computer Dictionary**: Broad range of computer/technology terms in accessible format
- **ECCMA Open Technical Dictionary (eOTD)**: ISO 22745 compliant technical dictionary for cataloging concepts
- **DevTerms**: Crowdsourced, open-source dictionary for developers ("Urban Dictionary for developers")

**Subject-Specific Resources**:
- **Open Concept Lab (OCL)**: Open-source terminology management with REST API (healthcare focus)
- **FreeDict**: Free bilingual dictionaries in generic XML format
- **Glossary of Digital Library Terms**: California Digital Library definitions
- **NNLM Data Glossary**: Network of National Library of Medicine data concepts
- **FOSS Community Acronyms**: GitHub-hosted FOSS abbreviations and acronyms

**API Integration Options**:
- **Dictionary API**: Free API for word definitions, phonetics, and origins
- **Metalicious**: Open-source web-based data dictionary for metadata capture

### Example Workflow

```
New content added →
Build script runs →
Extract technical terms →
Check against glossary.json →
Add new terms to pending_definitions.json →
Update article_terms_map.json →
Generate Hugo data files →
Render with automatic links
```

## Success Metrics

1. **90% of technical terms** are automatically detected and linked
2. **Glossary grows by 20+ terms** per month through automation
3. **Every glossary entry** shows related articles
4. **Build time increase** stays under 10 seconds
5. **False positive rate** for term detection under 5%

## Open Questions

1. **Term Detection**: Use NLP library or curated pattern matching?
2. **Link Frequency**: Link every occurrence or just first per article/section?
3. **Definition Source**: Manual only or integrate with technical dictionaries?
4. **Tooltip vs Click**: Show definitions on hover or require click?
5. **Threshold**: Minimum frequency before a term gets added to glossary?
6. **Categories**: Organize glossary by topic or alphabetically?
7. **Complexity**: Is this worth the implementation effort vs manual glossary?

## Implementation Notes

This is an advanced feature that would significantly enhance the knowledge base functionality. The main challenge is balancing automation accuracy with the effort required to implement and maintain the system.

Consider starting with a simpler version:
1. Phase 1: Manual glossary with Hugo shortcodes for linking
2. Phase 2: Semi-automated term extraction with manual review
3. Phase 3: Full automation with smart linking

The system would work especially well with the Hugo Book theme's built-in glossary support and could integrate with the LLM Model Library for AI-specific terminology.

---

*PRD Created: 2025-09-14*
*Status: DRAFT - For Future Consideration*
*Priority: Low-Medium*
*Complexity: High*