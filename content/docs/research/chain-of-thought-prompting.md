---
title: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
date: 2025-09-16T12:00:00-00:00
draft: false
tags: ["Chain-of-Thought", "Prompting", "LLM", "Reasoning", "Google Research", "arXiv"]
categories: ["Research", "AI", "Prompting"]
description: "Foundational paper on Chain-of-Thought prompting that shows how generating intermediate reasoning steps dramatically improves LLM performance on complex reasoning tasks."
author: "Jeremy Longshore"
toc: true
weight: 10
---

# Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

## Paper Details

**Authors**: Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, Denny Zhou (Google Research)

**Publication**: arXiv:2201.11903 [cs.CL] (Submitted 28 Jan 2022, last revised 10 Jan 2023)

**PDF Link**: [https://arxiv.org/pdf/2201.11903](https://arxiv.org/pdf/2201.11903)

## Abstract

We explore how generating a chain of thought -- a series of intermediate reasoning steps -- significantly improves the ability of large language models to perform complex reasoning. In particular, we show how such reasoning abilities emerge naturally in sufficiently large language models via a simple method called chain-of-thought prompting, where a few chain of thought demonstrations are provided as exemplars in prompting.

## Key Contributions

### 1. **Chain-of-Thought Methodology**
- Introduces the concept of explicitly showing reasoning steps in prompts
- Demonstrates that providing "thinking out loud" examples dramatically improves performance
- Shows this works across diverse reasoning tasks

### 2. **Scale-Dependent Emergence**
- Chain-of-thought prompting only works with sufficiently large models (100B+ parameters)
- Smaller models don't benefit from this approach
- Suggests reasoning abilities are an emergent property of scale

### 3. **Broad Task Performance**
- **Arithmetic reasoning**: GSM8K, SVAMP, AQuA-RAT
- **Commonsense reasoning**: CommonsenseQA, StrategyQA
- **Symbolic reasoning**: Last letter concatenation, coin flip

## Impact & Significance

This paper fundamentally changed how we interact with large language models:

- **🎯 Practical Impact**: Chain-of-thought prompting became standard practice
- **📈 Performance Gains**: 10-50%+ improvement on reasoning benchmarks
- **🔬 Scientific Insight**: Revealed emergent reasoning capabilities at scale
- **🛠️ Tool Development**: Led to techniques like tree-of-thought, self-consistency

## Example Chain-of-Thought Prompt

```
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
Each can has 3 tennis balls. How many tennis balls does he have now?

A: Roger started with 5 balls. 2 cans of 3 tennis balls each is
6 tennis balls. 5 + 6 = 11. The answer is 11.

Q: The cafeteria had 23 apples. If they used 20 to make lunch and
bought 6 more, how many apples do they have?

A: The cafeteria had 23 apples originally. They used 20 to make lunch.
So they had 23 - 20 = 3. Then they bought 6 more apples, so they have
3 + 6 = 9. The answer is 9.
```

## Follow-up Research

This paper sparked numerous follow-up studies:

- **Self-Consistency Decoding** (Wang et al., 2022)
- **Tree of Thoughts** (Yao et al., 2023)
- **Program-Aided Language Models** (Gao et al., 2022)
- **Automatic Chain-of-Thought Prompting** (Zhang et al., 2022)

## Why This Matters for AI Engineering

- **Prompt Engineering**: Essential technique for any LLM application
- **Reasoning Tasks**: Critical for mathematical, logical, and analytical applications
- **Model Evaluation**: Standard benchmark for reasoning capabilities
- **System Design**: Influences how we structure AI-powered applications

---

*Added to StartAI Tools Research Collection on September 16, 2025*