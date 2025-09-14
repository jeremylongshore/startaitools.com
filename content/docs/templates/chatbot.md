---
title: "Build a Chatbot"
weight: 10
description: "Create an AI-powered chatbot in minutes"
---

# Build a Chatbot

Create your own AI chatbot with this simple template.

## Quick Start

```javascript
const OpenAI = require('openai');

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

async function chatbot(userMessage) {
  const response = await openai.chat.completions.create({
    model: "gpt-3.5-turbo",
    messages: [
      { role: "system", content: "You are a helpful assistant." },
      { role: "user", content: userMessage }
    ]
  });

  return response.choices[0].message.content;
}

// Example usage
chatbot("Hello, how are you?").then(console.log);
```

## Next Steps

- Add conversation history
- Implement streaming responses
- Add custom personality