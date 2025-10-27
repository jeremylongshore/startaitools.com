---
title: "NEO: How to Build Vision-Language Models That Actually Understand Images"
date: 2025-10-25T22:30:00-06:00
draft: false
tags: ["Vision-Language Models", "Multimodal AI", "Open Source", "Research", "Computer Vision"]
categories: ["Technical Deep-Dive", "AI Research", "Educational"]
description: "Complete guide to NEO: the native vision-language model that rivals GPT-4V with 100x less training data. Learn the architecture, training approach, and why native VLMs are the future."
---

On October 2025, researchers from S-Lab (NTU), Xi'an Jiaotong University, and SenseTime published NEO: a vision-language model that **matches GPT-4V performance** while using only 390 million training examples instead of billions.

More importantly, they proved native VLMs (vision and language from scratch) can compete with modular systems (bolting vision onto existing LLMs).

This isn't just an academic achievement. It's a blueprint for building efficient multimodal AI without Google-scale infrastructure.

## The Problem: Why Most Vision-Language Models Are Frankenstein Creations

Here's how 90% of vision-language models work today:

**Step 1**: Take a powerful image model (like CLIP or a vision transformer)
**Step 2**: Take a powerful language model (like GPT or LLaMA)
**Step 3**: Bolt them together with an "adapter" layer
**Step 4**: Hope they learn to talk to each other

**Examples**: GPT-4V, LLaVA, InternVL, Qwen-VL

### Why This Works (Sort Of)

**Pros**:
- Leverage pre-trained components (billions of dollars of training)
- Fast to build (weeks instead of years)
- Can swap components easily

**Cons**:
- Vision and language speak different "languages" internally
- Adapter layer is a bottleneck
- Not truly unified understanding
- Requires massive alignment datasets

### The Alternative: Native Vision-Language Models

What if you trained **one model** that understands pixels and words from the beginning?

**This is NEO's approach** - and it's working.

---

## What Makes NEO Different: Native Vision-Language Primitives

NEO doesn't bolt components together. It builds vision-language understanding **from the ground up** using three core innovations.

### Innovation 1: Native-RoPE (Rotary Position Embeddings)

**The Problem**:
- Text is 1D (sequence: "The cat sat on the mat")
- Images are 2D (grid: 512×512 pixels)
- Standard language models can't handle 2D position information

**NEO's Solution: Native-RoPE**

Allocates position information across three dimensions:
- **T (Temporal)**: Sequence position for text
- **H (Height)**: Row position for images
- **W (Width)**: Column position for images

**How it works**:
```
Text token "cat":
  T = 3 (third word)
  H = 0 (not an image)
  W = 0 (not an image)

Image patch at row 15, col 23:
  T = constant (same "time" for all patches)
  H = 15 (row 15)
  W = 23 (column 23)
```

**Result**: Model natively understands 2D spatial relationships in images while still processing text sequences properly.

### Innovation 2: Mixed Attention Strategy

Different content types need different attention patterns:

**For text**:
- Causal attention (can't see future words)
- Enables autoregressive generation
- "The cat [can't see sat, on, mat yet]"

**For images**:
- Bidirectional attention (can see entire image)
- Enables spatial understanding
- "Patch at (15,23) can see all other patches"

**NEO implements both simultaneously** - text gets causal, images get bidirectional.

**Impact**: +0.7% accuracy over pure causal attention across all benchmarks.

### Innovation 3: Pre-Buffer Architecture

**The challenge**: How to learn visual features without forgetting language?

**NEO's approach**:

**Stage 1 (Pre-training)**: Split the model temporarily
- **Pre-Buffer**: 12 layers learn visual encoding
- **LLM layers**: Frozen (preserve language knowledge)
- Train on 345M image-text pairs

**Stage 2 (Mid-training)**: Merge everything
- Pre-Buffer + LLM = unified model
- Train end-to-end on 40M high-quality examples
- Full vision-language integration

**Stage 3 (Fine-tuning)**: Optimize for tasks
- 4M instruction examples
- Visual QA, dialogue, mathematics, reasoning

**Why this works**:
- Preserves linguistic ability (frozen LLM during pre-training)
- Learns visual features efficiently (dedicated pre-Buffer)
- Unifies understanding (merged end-to-end training)

---

## Training NEO: How to Build a Vision-Language Model

### Stage 1: Pre-Training (345M Examples)

**Goal**: Learn to connect pixels to words

**Dataset Composition**:
| Source | Count | Purpose |
|--------|-------|---------|
| LAION-400M | 120M | Web-scale diversity |
| COYO-700M | 150M | High-quality captions |
| BLIP3o | 20M | Synthetic captions |
| OpenImages | 5M | Recaptioned with detail |
| LAION-COCO | 30M | Natural scenes |
| Wukong | 20M | Chinese + OCR text |

**Training setup**:
- Freeze LLM weights (preserve language)
- Train Pre-Buffer (12 layers) + adapter
- 3:7 language-to-multimodal data ratio
- Learning rate: 8×10⁻⁴
- Hardware: 128 GPUs (80GB each)

**What the model learns**:
- Basic object recognition
- Spatial relationships
- Text in images (OCR)
- Image-caption alignment

### Stage 2: Mid-Training (40M Examples)

**Goal**: Strengthen vision-language reasoning

**Dataset Composition**:
| Task Type | Percentage | Examples |
|-----------|-----------|----------|
| Image Captioning | 66% | Describe this image |
| Conversation | 11% | Multi-turn dialogue |
| Detection | 8% | Find objects/regions |
| OCR | 15% | Read text in images |

**Training changes**:
- Unfreeze everything (end-to-end optimization)
- Merge Pre-Buffer into unified architecture
- Learning rate: 4×10⁻⁵ (lower for stability)
- Resolution: 256×256 to 2,048×2,048

**What the model learns**:
- Complex reasoning
- Multi-turn conversations
- Precise localization
- Document understanding

### Stage 3: Supervised Fine-Tuning (4M Examples)

**Goal**: Master specific tasks

**Dataset Composition**:
- Visual question answering
- Multimodal dialogue
- Mathematical reasoning
- Knowledge-intensive QA
- Bilingual (English + Chinese)

**Training setup**:
- Learning rate: 5×10⁻⁵
- Full high-resolution support
- Task-specific optimization

**What the model learns**:
- Following instructions precisely
- Answering complex questions
- Mathematical problem-solving
- Cross-lingual understanding

---

## Performance: NEO vs. The World

### NEO-2.2B (Lightweight Model)

| Benchmark | NEO-2.2B | InternVL2.5 (2B) | Difference |
|-----------|----------|------------------|------------|
| **MMMU** (reasoning) | 48.6 | 48.6 | Tied |
| **MMBench** (general) | 76.0 | 74.7 | +1.3 ✅ |
| **MMVet** (real-world) | 49.6 | 50.3 | -0.7 |
| **ChartQA** (charts) | 81.2 | 79.1 | +2.1 ✅ |
| **TextVQA** (OCR) | 74.0 | 71.5 | +2.5 ✅ |

**Key insight**: Native 2B model matches or beats modular 2B models despite simpler architecture.

### NEO-9B (Larger Model)

| Benchmark | NEO-9B | InternVL3 (8B) | Difference |
|-----------|--------|----------------|------------|
| **MMMU** | 54.6 | 62.7 | -8.1 |
| **MMBench** | 82.1 | 83.4 | -1.3 |
| **SEED-Bench** | 76.3 | 76.2 | +0.1 ✅ |
| **ChartQA** | 82.1 | 83.9 | -1.8 |
| **DocVQA** | 88.6 | 90.6 | -2.0 |

**Key insight**: Competitive with larger modular models, room for improvement on knowledge-intensive tasks.

### The Training Data Difference

**NEO**: 390M total training examples
**Typical Modular VLM**: 1-5B+ training examples

**NEO achieves 90-95% of modular VLM performance with 10-20x less training data.**

Why? Native architecture is more efficient - no alignment overhead between separate vision/language components.

---

## Architecture Deep-Dive: How NEO Actually Works

### Input Processing

**For text input**: "Describe this image"
```python
# Tokenize text
tokens = tokenizer("Describe this image")
# Output: [Describe, this, image]

# Add position embeddings
for i, token in enumerate(tokens):
    token.T = i  # Sequence position
    token.H = 0  # Not an image
    token.W = 0  # Not an image
```

**For image input**: 512×512 photo
```python
# Divide into 32×32 patches (16×16 stride)
patches = image.to_patches(patch_size=16)
# Output: 32×32 = 1,024 patches

# Add position embeddings
for row in range(32):
    for col in range(32):
        patch = patches[row][col]
        patch.T = 0  # Constant for all patches
        patch.H = row  # Row position
        patch.W = col  # Column position
```

### Unified Token Sequence

After processing, NEO sees:
```
[Describe, this, image, <patch_0_0>, <patch_0_1>, ..., <patch_31_31>]
 ^text^   ^text^ ^text^  ^image patches (1,024 total)^
```

All tokens flow through the same transformer layers.

### Attention Mechanism

```python
# Mixed attention based on token type
for token in sequence:
    if token.is_text:
        # Causal attention (can't see future)
        attention_mask = causal_mask(token.position)
    elif token.is_image:
        # Bidirectional attention (can see all patches)
        attention_mask = full_mask()

    # Apply attention with appropriate mask
    output = attention(token, mask=attention_mask)
```

### Generation Process

**User**: "What's in this image?"
**NEO**:
1. Processes image patches (bidirectional attention)
2. Processes text question (causal attention)
3. Generates answer token-by-token (causal attention)
4. Each new token attends to all previous tokens + all image patches

**Output**: "The image shows a golden retriever playing in a park with a red ball."

---

## How to Use NEO: Practical Guide

### Installation

```bash
# Clone repository
git clone https://github.com/EvolvingLMMs-Lab/NEO.git
cd NEO

# Install dependencies
pip install -r requirements.txt

# Download model weights (Hugging Face)
# NEO-2B: https://huggingface.co/EvolvingLMMs-Lab/NEO-2B-SFT
# NEO-9B: https://huggingface.co/EvolvingLMMs-Lab/NEO-9B-SFT
```

### Basic Usage

```python
from transformers import AutoModel, AutoTokenizer
from PIL import Image

# Load model
model = AutoModel.from_pretrained("EvolvingLMMs-Lab/NEO-2B-SFT")
tokenizer = AutoTokenizer.from_pretrained("EvolvingLMMs-Lab/NEO-2B-SFT")

# Load image
image = Image.open("example.jpg")

# Ask question
question = "What's in this image?"

# Generate response
response = model.generate(
    image=image,
    text=question,
    max_length=200
)

print(response)
# Output: "The image shows a golden retriever playing..."
```

### Advanced Usage: Multi-Turn Conversation

```python
# Start conversation
conversation = []

# Turn 1
conversation.append({
    "role": "user",
    "content": "What color is the dog?",
    "image": image
})

response1 = model.generate(conversation)
# Output: "The dog is golden/tan colored."

conversation.append({
    "role": "assistant",
    "content": response1
})

# Turn 2 (continues conversation)
conversation.append({
    "role": "user",
    "content": "What is it holding?"
})

response2 = model.generate(conversation)
# Output: "The dog is holding a red ball in its mouth."
```

### Custom Fine-Tuning

```python
from neo.training import train

# Prepare your dataset
dataset = [
    {
        "image": "path/to/image1.jpg",
        "conversations": [
            {"role": "user", "content": "Question about image?"},
            {"role": "assistant", "content": "Answer based on image."}
        ]
    },
    # ... more examples
]

# Fine-tune on your domain
train(
    model="EvolvingLMMs-Lab/NEO-2B-SFT",
    dataset=dataset,
    epochs=3,
    learning_rate=5e-5,
    output_dir="./finetuned_model"
)
```

---

## Use Cases: What You Can Build with NEO

### 1. Visual Question Answering System

**Example**: Customer support for e-commerce

```python
# Customer uploads product image
image = customer_upload("broken_product.jpg")

# Ask: "What's wrong with this product?"
diagnosis = neo.generate(
    image=image,
    text="Analyze this product image and identify any defects or damage."
)

# Output: "The product shows a crack on the left side of the casing..."
```

**Value**: Automated visual triage before human support

### 2. Document Understanding

**Example**: Invoice processing

```python
# Process scanned invoice
invoice_image = Image.open("invoice_2025.jpg")

# Extract information
data = neo.generate(
    image=invoice_image,
    text="Extract the invoice number, date, total amount, and line items from this invoice. Return as JSON."
)

# Output: {"invoice_number": "INV-2025-001", "date": "2025-10-25", ...}
```

**Value**: 10-100x faster than manual data entry

### 3. Medical Image Analysis

**Example**: Radiology assistance

```python
# X-ray image
xray = Image.open("chest_xray.jpg")

# Analysis
findings = neo.generate(
    image=xray,
    text="Describe any abnormalities visible in this chest X-ray. Note: This is for educational purposes only."
)

# Output: "The image shows signs of possible infiltration in the lower right lobe..."
```

**Value**: Pre-screening to prioritize urgent cases

### 4. Content Moderation

**Example**: Social media safety

```python
# User-uploaded image
user_image = Image.open("user_post.jpg")

# Check for violations
moderation = neo.generate(
    image=user_image,
    text="Analyze this image for: violence, explicit content, hate symbols, or dangerous activities. Return risk level (low/medium/high) and explanation."
)

# Output: {"risk": "low", "explanation": "Image shows a landscape photo..."}
```

**Value**: Automated first-pass moderation

### 5. Educational Assistant

**Example**: Homework help

```python
# Student uploads math problem photo
problem_image = Image.open("math_problem.jpg")

# Solve step-by-step
solution = neo.generate(
    image=problem_image,
    text="Solve this math problem step by step, explaining each step clearly."
)

# Output: "Step 1: Identify the equation... Step 2: Isolate the variable..."
```

**Value**: 24/7 tutoring assistance

---

## Limitations & When NOT to Use NEO

### 1. Knowledge-Intensive Tasks

**Problem**: NEO underperforms on MMMU (reasoning benchmark) compared to GPT-4V

**Example**:
- ❌ "Explain the historical significance of this architectural style"
- ✅ "What architectural elements are visible in this building?"

**Why**: Training corpus emphasizes visual-linguistic alignment over encyclopedic knowledge

**Mitigation**: Combine with RAG (Retrieval-Augmented Generation) for knowledge queries

### 2. Very High-Resolution Images

**Problem**: Computational cost scales with image resolution

**Current support**: Up to 2,048×2,048 pixels
**Practical limit**: ~1,024×1,024 for real-time inference

**Workaround**: Tile large images or use image pyramids

### 3. Real-Time Video Analysis

**Problem**: Not optimized for video streams

**Current**: Single image processing
**Missing**: Temporal modeling across frames

**Alternative**: Process keyframes separately, use specialized video models

### 4. Highly Specialized Domains (Out-of-the-Box)

**Problem**: General training data doesn't cover niche domains

**Examples**:
- Satellite imagery analysis
- Microscopy images
- Industrial defect detection

**Solution**: Fine-tune on domain-specific data (hundreds to thousands of examples)

---

## NEO vs. Competition: What's Different?

### NEO vs. LLaVA

| Aspect | NEO | LLaVA |
|--------|-----|-------|
| **Architecture** | Native (unified) | Modular (CLIP + LLaMA) |
| **Position Encoding** | Native-RoPE (2D spatial) | 1D sequence only |
| **Attention** | Mixed (causal + bidirectional) | Pure causal |
| **Training Data** | 390M examples | 1.2M (LLaVA-1.5) |
| **Performance** | Competitive | Strong baseline |

**Winner**: NEO for efficiency, LLaVA for simplicity

### NEO vs. GPT-4V

| Aspect | NEO | GPT-4V |
|--------|-----|--------|
| **Access** | Open source | Closed API |
| **Cost** | Self-host ($0-200/month) | $0.01-0.10 per image |
| **Customization** | Full fine-tuning | Prompt engineering only |
| **Performance** | 85-90% of GPT-4V | Best-in-class |
| **Latency** | <2s (local GPU) | 3-10s (API call) |

**Winner**: GPT-4V for performance, NEO for control/cost

### NEO vs. InternVL

| Aspect | NEO | InternVL |
|--------|-----|----------|
| **Architecture** | Native | Modular |
| **Model Sizes** | 2B, 9B | 2B, 8B, 26B |
| **Training Data** | 390M | 1B+ |
| **Performance** | 90-95% of InternVL | State-of-the-art |
| **Resource Requirements** | Lower | Higher |

**Winner**: Tie - different trade-offs for different needs

---

## The Research Implications: Why This Matters

### 1. Native VLMs Are Viable

**Previous belief**: Need separate vision encoders (CLIP, ViT) to match modular VLMs

**NEO proves**: Native architecture with proper primitives (Native-RoPE, mixed attention) can compete

**Impact**: Simplifies VLM development, reduces engineering complexity

### 2. Data Efficiency Through Architecture

**Key finding**: NEO achieves 90-95% performance with 10-20x less training data

**Why**: Native architecture doesn't waste capacity on vision-language alignment

**Implication**: Smaller teams can build competitive VLMs without Google-scale compute

### 3. Reusable Components

**NEO releases**:
- Pre-Buffer architecture (drop-in visual encoding)
- Native-RoPE implementation (position encoding)
- Mixed attention mechanisms

**Value**: Other researchers can build on these primitives

### 4. Future of Multimodal AI

**Trend**: Moving from modular (bolt components together) to native (integrated from scratch)

**Examples**:
- Text + images (NEO)
- Text + audio (Gemini)
- Text + images + audio + video (future)

**NEO provides roadmap** for building truly unified multimodal models

---

## Implementation Guide: Building Your Own NEO-Based System

### Week 1: Setup and Testing

**Day 1-2: Environment setup**
```bash
# Clone repository
git clone https://github.com/EvolvingLMMs-Lab/NEO.git

# Install dependencies
pip install -r requirements.txt
pip install torch torchvision transformers

# Download model weights
huggingface-cli download EvolvingLMMs-Lab/NEO-2B-SFT
```

**Day 3-4: Test basic functionality**
```python
# Run provided examples
python examples/image_qa.py
python examples/conversation.py
python examples/document_understanding.py

# Benchmark on your hardware
python benchmark.py --model NEO-2B-SFT --batch-size 1
```

**Day 5: Evaluate on your domain**
```python
# Prepare test set (50-100 examples)
test_data = load_your_domain_images()

# Run evaluation
results = evaluate_model(
    model="NEO-2B-SFT",
    test_data=test_data,
    metrics=["accuracy", "latency", "memory"]
)
```

**Decision point**: Proceed if accuracy >70% on your test set

### Week 2: Fine-Tuning (If Needed)

**Prepare training data**:
```python
# Format: JSON with image paths and conversations
training_data = [
    {
        "image": "path/to/image1.jpg",
        "conversations": [
            {"role": "user", "content": "Question?"},
            {"role": "assistant", "content": "Answer."}
        ]
    },
    # 500-5,000 examples recommended
]
```

**Fine-tune model**:
```bash
python train.py \
    --model NEO-2B-SFT \
    --data training_data.json \
    --epochs 3 \
    --learning-rate 5e-5 \
    --batch-size 4 \
    --output finetuned_neo
```

**Evaluate improvement**:
```python
# Compare base vs. fine-tuned
base_results = evaluate("NEO-2B-SFT", test_data)
finetuned_results = evaluate("finetuned_neo", test_data)

print(f"Improvement: {finetuned_results.accuracy - base_results.accuracy:.1%}")
```

### Week 3: Production Deployment

**Option 1: Local deployment**
```python
from flask import Flask, request
import torch

app = Flask(__name__)
model = load_neo_model("finetuned_neo")

@app.route('/analyze', methods=['POST'])
def analyze_image():
    image = request.files['image']
    question = request.form['question']

    response = model.generate(
        image=image,
        text=question,
        max_length=200
    )

    return {"answer": response}

app.run(host='0.0.0.0', port=8000)
```

**Option 2: Cloud deployment (AWS/GCP)**
```yaml
# docker-compose.yml
version: '3'
services:
  neo-api:
    image: neo-api:latest
    ports:
      - "8000:8000"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

**Option 3: Serverless (Modal, RunPod)**
```python
import modal

stub = modal.Stub("neo-inference")

@stub.function(
    gpu="A10G",
    image=modal.Image.debian_slim().pip_install("transformers", "torch")
)
def generate(image_url: str, question: str):
    model = load_neo_model()
    return model.generate(image_url, question)
```

### Week 4: Monitoring and Optimization

**Set up monitoring**:
```python
import prometheus_client as prom

# Track metrics
inference_time = prom.Histogram('neo_inference_seconds', 'Time to generate response')
accuracy_gauge = prom.Gauge('neo_accuracy', 'Model accuracy on validation set')
error_counter = prom.Counter('neo_errors_total', 'Total errors')

# Monitor in production
@inference_time.time()
def monitored_generate(image, text):
    try:
        response = model.generate(image, text)
        return response
    except Exception as e:
        error_counter.inc()
        raise
```

**Optimize performance**:
```python
# Enable mixed precision
model = model.half()  # FP16 inference

# Batch processing
images = [image1, image2, image3]
questions = [q1, q2, q3]
responses = model.generate_batch(images, questions)

# Quantization (if needed)
from torch.quantization import quantize_dynamic
model = quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
```

---

## Cost Analysis: Running NEO in Production

### Infrastructure Costs

**NEO-2.2B (Lightweight)**:
- **GPU**: RTX 4090 (24GB) or A10G (24GB)
- **Cloud cost**: $0.50-1.50/hour (AWS/GCP spot instances)
- **Self-hosted**: ~$1,500-2,000 (consumer GPU) or $10K-15K (data center GPU)

**NEO-9B (Full-size)**:
- **GPU**: A100 (40GB) or H100 (80GB)
- **Cloud cost**: $2-5/hour (AWS/GCP spot instances)
- **Self-hosted**: ~$30K-50K (data center GPU)

### Operational Costs (Monthly)

**Small scale (1,000 requests/day)**:
- Cloud GPU rental: $360-1,080/month
- Bandwidth: $10-50/month
- Storage: $5-10/month
- **Total**: $375-1,140/month

**Medium scale (10,000 requests/day)**:
- Cloud GPU rental: $720-2,160/month (2-4 instances)
- Bandwidth: $50-200/month
- Storage: $20-50/month
- **Total**: $790-2,410/month

**Large scale (100,000 requests/day)**:
- Cloud GPU rental: $3,600-10,800/month (10-20 instances + load balancer)
- Bandwidth: $200-1,000/month
- Storage: $100-500/month
- **Total**: $3,900-12,300/month

### Cost Comparison: NEO vs. API Services

**Scenario**: 10,000 image analysis requests/month

| Service | Cost per Request | Monthly Cost | Notes |
|---------|------------------|--------------|-------|
| **GPT-4V API** | $0.01-0.10 | $100-1,000 | Variable pricing |
| **Google Gemini** | $0.002-0.02 | $20-200 | Cheaper but less capable |
| **NEO Self-Hosted** | $0.01-0.05 | $100-500 | Fixed GPU rental |
| **NEO Cloud (spot)** | $0.02-0.08 | $200-800 | Scalable |

**Breakeven analysis**:
- <5K requests/month: Use APIs (simpler)
- 5K-50K requests/month: Consider self-hosting
- >50K requests/month: Self-host wins (10-50x cheaper)

---

## The Bottom Line: When to Use NEO

### ✅ Use NEO When:

**1. You need control**
- Fine-tune on proprietary data
- Custom deployment requirements
- Data privacy regulations (HIPAA, GDPR)

**2. You need cost efficiency at scale**
- >10K requests/day
- Long-term production deployment
- Predictable costs matter

**3. You need low latency**
- Real-time applications (<2s response)
- Edge deployment (on-device)
- Batch processing large volumes

**4. You want cutting-edge research**
- Building next-gen multimodal systems
- Experimenting with native VLM architectures
- Contributing to open research

### ❌ Don't Use NEO When:

**1. You need the absolute best performance**
- GPT-4V still wins on complex reasoning
- InternVL3 better on knowledge-intensive tasks

**2. You have low volume**
- <1K requests/month: API services cheaper and simpler
- No need to manage infrastructure

**3. You need video understanding**
- NEO optimized for images, not video streams
- Use specialized video models

**4. You lack technical resources**
- No ML engineering team
- No GPU infrastructure
- Prefer managed services

---

## Learning Resources & Next Steps

### Official Resources
- **Paper**: [arXiv:2510.14979](https://arxiv.org/abs/2510.14979)
- **Code**: [GitHub - EvolvingLMMs-Lab/NEO](https://github.com/EvolvingLMMs-Lab/NEO)
- **Models**: [Hugging Face - NEO](https://huggingface.co/EvolvingLMMs-Lab)

### Hands-On Tutorials
1. **Getting Started**: Run NEO in 10 minutes
2. **Fine-Tuning Guide**: Adapt to your domain
3. **Production Deployment**: Scale to thousands of requests/day

### Community
- **GitHub Issues**: Report bugs, request features
- **Hugging Face Forums**: Ask questions, share results
- **Research Discord**: Discuss with researchers

### Related Reading on StartAITools
- [PokeeResearch-7B: Training AI Agents Without $100K Annotations](/posts/pokeeresearch-7b-reinforcement-learning-ai-research-agent/)
- [Building Production-Ready Research Tool](/posts/building-production-ready-research-tool-outperforms-anthropic/)
- [Coasean Singularity: AI Agents Transform Markets](/posts/coasean-singularity-ai-agents-market-transformation/)

---

## Key Takeaways

1. **Native VLMs are viable** - NEO proves unified architecture can compete with modular systems
2. **Data efficiency matters** - 390M examples rivals models trained on billions
3. **Open source wins** - Full control, customization, and no API costs
4. **Architecture innovation** - Native-RoPE + mixed attention = core primitives for future VLMs
5. **Production ready** - 2B and 9B models deployable today

**Bottom line**: NEO democratizes vision-language AI. You don't need Google-scale resources to build powerful multimodal systems anymore.

**What you can do this weekend**:
1. Clone the repo: `git clone https://github.com/EvolvingLMMs-Lab/NEO.git`
2. Download NEO-2B: Test on your images
3. Evaluate on your domain: See if it works for your use case
4. Fine-tune (if needed): 500-5K examples for domain adaptation

The future of multimodal AI is native, efficient, and open. NEO shows the way.

---

**Questions? Feedback?**

Tried NEO and have results to share?
- **Twitter/X**: [@jeremylongshore](https://x.com/jeremylongshore)
- **Email**: jeremy@intentsolutions.io
- **GitHub**: [EvolvingLMMs-Lab/NEO](https://github.com/EvolvingLMMs-Lab/NEO)

---

*Published: October 25, 2025*
*Author: Jeremy Longshore*
*Reading time: 25 minutes*
*Paper: From Pixels to Words (arXiv:2510.14979)*
*Code: Apache 2.0 License*
