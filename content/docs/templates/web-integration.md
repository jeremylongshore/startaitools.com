---
title: "Add AI to Your Website"
weight: 20
description: "Integrate AI features into any website"
---

# Add AI to Your Website

Quick integration guide for adding AI to your existing site.

## Frontend Integration

```html
<!-- Add to your HTML -->
<div id="ai-chat"></div>

<script>
async function askAI(question) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: question })
  });

  const data = await response.json();
  return data.reply;
}
</script>
```

## Backend API

```javascript
// Express.js example
app.post('/api/chat', async (req, res) => {
  const { message } = req.body;

  const reply = await openai.chat.completions.create({
    model: "gpt-3.5-turbo",
    messages: [{ role: "user", content: message }]
  });

  res.json({ reply: reply.choices[0].message.content });
});
```

## Next Steps
- Add authentication
- Implement rate limiting
- Create custom UI components