---
title: "Quick Start"
weight: 1
bookToc: true
---

# Quick Start

Get your first AI integration running in 5 minutes.

## Prerequisites

- Node.js 18+ or Python 3.8+
- API key from OpenAI, Anthropic, or Google
- Text editor (VS Code recommended)

## Installation

### Option 1: Node.js

```bash
npm init -y
npm install openai
```

### Option 2: Python

```bash
pip install openai
```

## Your First AI Integration

Create a file called `app.js` (Node.js) or `app.py` (Python):

### Node.js Example

```javascript
const OpenAI = require('openai');

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

async function main() {
  const completion = await openai.chat.completions.create({
    model: "gpt-3.5-turbo",
    messages: [
      { role: "user", content: "Write a haiku about coding" }
    ]
  });

  console.log(completion.choices[0].message.content);
}

main();
```

### Python Example

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Write a haiku about coding"}
    ]
)

print(completion.choices[0].message.content)
```

## Set Your API Key

### Linux/Mac
```bash
export OPENAI_API_KEY='your-api-key-here'
```

### Windows
```cmd
set OPENAI_API_KEY=your-api-key-here
```

## Run Your Code

```bash
# Node.js
node app.js

# Python
python app.py
```

## Next Steps

- [Build a Chatbot](/docs/templates/chatbot/)
- [Add AI to Your Website](/docs/templates/web-integration/)
- [Process Documents with AI](/docs/templates/document-processor/)

## Common Issues

### API Key Not Found
Make sure your environment variable is set correctly. Test with:
```bash
echo $OPENAI_API_KEY
```

### Rate Limits
Free tier has limits. Add delays between requests or upgrade your plan.

### Connection Errors
Check your internet connection and firewall settings.

---

**Need help?** Check our [templates](/docs/templates/) for ready-to-use examples.