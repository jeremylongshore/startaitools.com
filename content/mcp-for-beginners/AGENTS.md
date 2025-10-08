# AGENTS.md

## Project Overview

**MCP for Beginners** is an open-source educational curriculum for learning the Model Context Protocol (MCP) - a standardized framework for interactions between AI models and client applications. This repository provides comprehensive learning materials with hands-on code examples across multiple programming languages.

### Key Technologies

- **Programming Languages**: C#, Java, JavaScript, TypeScript, Python, Rust
- **Frameworks & SDKs**: 
  - MCP SDK (`@modelcontextprotocol/sdk`)
  - Spring Boot (Java)
  - FastMCP (Python)
  - LangChain4j (Java)
- **Databases**: PostgreSQL with pgvector extension
- **Cloud Platforms**: Azure (Container Apps, OpenAI, Content Safety, Application Insights)
- **Build Tools**: npm, Maven, pip, Cargo
- **Documentation**: Markdown with automated multi-language translation (48+ languages)

### Architecture

- **11 Core Modules (00-11)**: Sequential learning path from fundamentals to advanced topics
- **Hands-on Labs**: Practical exercises with complete solution code in multiple languages
- **Sample Projects**: Working MCP server and client implementations
- **Translation System**: Automated GitHub Actions workflow for multi-language support
- **Image Assets**: Centralized images directory with translated versions

## Setup Commands

This is a documentation-focused repository. Most setup occurs within individual sample projects and labs.

### Repository Setup

```bash
# Clone the repository
git clone https://github.com/microsoft/mcp-for-beginners.git
cd mcp-for-beginners
```

### Working with Sample Projects

Sample projects are located in:
- `03-GettingStarted/samples/` - Language-specific examples
- `03-GettingStarted/01-first-server/solution/` - First server implementations
- `03-GettingStarted/02-client/solution/` - Client implementations
- `11-MCPServerHandsOnLabs/` - Comprehensive database integration labs

Each sample project contains its own setup instructions:

#### TypeScript/JavaScript Projects
```bash
cd <project-directory>
npm install
npm start
```

#### Python Projects
```bash
cd <project-directory>
pip install -r requirements.txt
# or
pip install -e .
python main.py
```

#### Java Projects
```bash
cd <project-directory>
mvn clean install
mvn spring-boot:run
```

## Development Workflow

### Documentation Structure

- **Modules 00-11**: Core curriculum content in sequential order
- **translations/**: Language-specific versions (auto-generated, do not edit directly)
- **translated_images/**: Localized image versions (auto-generated)
- **images/**: Source images and diagrams

### Making Documentation Changes

1. Edit only the English markdown files in the root module directories (00-11)
2. Update images in the `images/` directory if needed
3. The co-op-translator GitHub Action will automatically generate translations
4. Translations are regenerated on push to main branch

### Working with Translations

- **Automated Translation**: GitHub Actions workflow handles all translations
- **Do NOT manually edit** files in `translations/` directory
- Translation metadata is embedded in each translated file
- Supported languages: 48+ languages including Arabic, Chinese, French, German, Hindi, Japanese, Korean, Portuguese, Russian, Spanish, and many more

## Testing Instructions

### Documentation Validation

Since this is primarily a documentation repository, testing focuses on:

1. **Link Validation**: Ensure all internal links work
```bash
# Check for broken markdown links
find . -name "*.md" -type f | xargs grep -n "\[.*\](.*)"
```

2. **Code Sample Validation**: Test that code examples compile/run
```bash
# Navigate to specific sample and run its tests
cd 03-GettingStarted/samples/typescript
npm install && npm test
```

3. **Markdown Linting**: Check formatting consistency
```bash
# Use markdownlint if needed
npx markdownlint-cli2 "**/*.md" "#node_modules"
```

### Sample Project Testing

Each language-specific sample includes its own testing approach:

#### TypeScript/JavaScript
```bash
npm test
npm run build
```

#### Python
```bash
pytest
python -m pytest tests/
```

#### Java
```bash
mvn test
mvn verify
```

## Code Style Guidelines

### Documentation Style

- Use clear, beginner-friendly language
- Include code examples in multiple languages where applicable
- Follow markdown best practices:
  - Use ATX-style headers (`#` syntax)
  - Use fenced code blocks with language identifiers
  - Include descriptive alt text for images
  - Keep line lengths reasonable (no hard limit, but be sensible)

### Code Sample Style

#### TypeScript/JavaScript
- Use ES modules (`import`/`export`)
- Follow TypeScript strict mode conventions
- Include type annotations
- Target ES2022

#### Python
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Include docstrings for functions and classes
- Use modern Python features (3.8+)

#### Java
- Follow Spring Boot conventions
- Use Java 21 features
- Follow standard Maven project structure
- Include Javadoc comments

### File Organization

```
<module-number>-<ModuleName>/
├── README.md              # Main module content
├── samples/               # Code examples (if applicable)
│   ├── typescript/
│   ├── python/
│   ├── java/
│   └── ...
└── solution/              # Complete working solutions
    └── <language>/
```

## Build and Deployment

### Documentation Deployment

The repository uses GitHub Pages or similar for documentation hosting (if applicable). Changes to the main branch trigger:

1. Translation workflow (`.github/workflows/co-op-translator.yml`)
2. Automated translation of all English markdown files
3. Image localization as needed

### No Build Process Required

This repository primarily contains markdown documentation. No compilation or build step is needed for the core curriculum content.

### Sample Project Deployment

Individual sample projects may have deployment instructions:
- See `03-GettingStarted/09-deployment/` for MCP server deployment guidance
- Azure Container Apps deployment examples in `11-MCPServerHandsOnLabs/`

## Contributing Guidelines

### Pull Request Process

1. **Fork and Clone**: Fork the repository and clone your fork locally
2. **Create a Branch**: Use descriptive branch names (e.g., `fix/typo-module-3`, `add/python-example`)
3. **Make Changes**: Edit English markdown files only (not translations)
4. **Test Locally**: Verify markdown renders correctly
5. **Submit PR**: Use clear PR titles and descriptions
6. **CLA**: Sign the Microsoft Contributor License Agreement when prompted

### PR Title Format

Use clear, descriptive titles:
- `[Module XX] Brief description` for module-specific changes
- `[Samples] Description` for sample code changes
- `[Docs] Description` for general documentation updates

### What to Contribute

- Bug fixes in documentation or code samples
- New code examples in additional languages
- Clarifications and improvements to existing content
- New case studies or practical examples
- Issue reports for unclear or incorrect content

### What NOT to Do

- Do not directly edit files in `translations/` directory
- Do not edit `translated_images/` directory
- Do not add large binary files without discussion
- Do not change translation workflow files without coordination

## Additional Notes

### Repository Maintenance

- **Changelog**: All significant changes are documented in `changelog.md`
- **Study Guide**: Use `study_guide.md` for curriculum navigation overview
- **Issue Templates**: Use GitHub issue templates for bug reports and feature requests
- **Code of Conduct**: All contributors must follow the Microsoft Open Source Code of Conduct

### Learning Path

Follow modules in sequential order (00-11) for optimal learning:
1. **00-02**: Fundamentals (Introduction, Core Concepts, Security)
2. **03**: Getting Started with hands-on implementation
3. **04-05**: Practical implementation and advanced topics
4. **06-10**: Community, best practices, and real-world applications
5. **11**: Comprehensive database integration labs (13 sequential labs)

### Support Resources

- **Documentation**: https://modelcontextprotocol.io/
- **Specification**: https://spec.modelcontextprotocol.io/
- **Community**: https://github.com/orgs/modelcontextprotocol/discussions
- **Discord**: Microsoft Azure AI Foundry Discord server
- **Related Courses**: See README.md for other Microsoft learning paths

### Common Troubleshooting

**Q: My PR is failing the translation check**
A: Ensure you only edited English markdown files in the root module directories, not translated versions.

**Q: How do I add a new language?**
A: Language support is managed through the co-op-translator workflow. Open an issue to discuss adding new languages.

**Q: Code samples aren't working**
A: Ensure you've followed the setup instructions in the specific sample's README. Check that you have the correct versions of dependencies installed.

**Q: Images aren't displaying**
A: Verify image paths are relative and use forward slashes. Images should be in the `images/` directory or `translated_images/` for localized versions.

### Performance Considerations

- Translation workflow may take several minutes to complete
- Large images should be optimized before committing
- Keep individual markdown files focused and reasonably sized
- Use relative links for better portability

### Project Governance

This project follows Microsoft open source practices:
- MIT License for code and documentation
- Microsoft Open Source Code of Conduct
- CLA required for contributions
- Security issues: Follow SECURITY.md guidelines
- Support: See SUPPORT.md for help resources
