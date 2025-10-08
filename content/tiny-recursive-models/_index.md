---
title: "Tiny Recursive Models: Less is More"
date: 2025-10-08T08:30:00-06:00
draft: false
---

# Less is More: Recursive Reasoning with Tiny Networks

**Research by Samsung SAIL Montreal**

Achieving 45% on ARC-AGI-1 and 8% on ARC-AGI-2 using only a **7M parameter neural network**.

---

## About This Research

**Tiny Recursion Model (TRM)** is a breakthrough in recursive reasoning that challenges the assumption that massive foundational models are necessary for complex problem-solving. This research demonstrates that "less is more" - a tiny model pretrained from scratch, recursing on itself and updating its answers over time, can achieve remarkable results without requiring massive computational resources.

**Original Authors:** Samsung SAIL Montreal Research Team
**Paper:** [Less is More: Recursive Reasoning with Tiny Networks](https://arxiv.org/abs/2510.04871)
**Source Repository:** [Samsung SAIL Montreal GitHub](https://github.com/SamsungSAILMontreal/TinyRecursiveModels)
**Hosted with permission for educational purposes on StartAITools.com**

---

## Key Achievements

**Performance Metrics:**
- **45% accuracy on ARC-AGI-1** - competitive with large language models
- **8% accuracy on ARC-AGI-2** - state-of-the-art for small models
- **Only 7M parameters** - vs billions in traditional LLMs

**Breakthrough Insight:**
> "The idea that one must rely on massive foundational models trained for millions of dollars by some big corporation in order to achieve success on hard tasks is a trap. Currently, there is too much focus on exploiting LLMs rather than devising and expanding new lines of direction."

---

## How TRM Works

Tiny Recursion Model (TRM) recursively improves its predicted answer **y** with a tiny network:

1. **Starts with:** Embedded input question **x**, initial embedded answer **y**, and latent **z**
2. **For K improvement steps:**
   - Recursively updates latent **z** given question **x**, current answer **y**, and current latent **z** (recursive reasoning)
   - Updates answer **y** given current answer **y** and current latent **z**
3. **Result:** Progressive answer improvement in extremely parameter-efficient manner while minimizing overfitting

![TRM Architecture](https://AlexiaJM.github.io/assets/images/TRM_fig.png)

---

## Research Motivation

This work builds on the Hierarchical Reasoning Model (HRM) but **simplifies recursive reasoning to its core essence**:

**Improvements over HRM:**
- ✅ Simplified architecture (no biological brain analogies needed)
- ✅ No mathematical fixed-point theorem required
- ✅ No hierarchical structure necessary
- ✅ Core recursive reasoning extracted and optimized

**Philosophy:**
> "Recursive reasoning ultimately has nothing to do with the human brain, does not require any mathematical (fixed-point) theorem, nor any hierarchy."

---

## Repository Contents

### Core Implementation
- **`pretrain.py`** - Main training script for TRM models
- **`arch/`** - Model architecture implementations
- **`dataset/`** - Dataset preparation and augmentation utilities

### Supported Datasets
- **ARC-AGI-1** - Abstract Reasoning Challenge (original)
- **ARC-AGI-2** - Abstract Reasoning Challenge (updated)
- **Sudoku-Extreme** - Complex Sudoku puzzles
- **Maze-Hard** - Challenging maze navigation

### Requirements
- Python 3.10+
- CUDA 12.6.0+
- PyTorch (nightly builds)
- Weights & Biases (optional for logging)

---

## Quick Start

### Installation

```bash
pip install --upgrade pip wheel setuptools
pip install --pre --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu126
pip install -r requirements.txt
pip install --no-cache-dir --no-build-isolation adam-atan2
```

### Dataset Preparation

```bash
# ARC-AGI-1
python -m dataset.build_arc_dataset \
  --input-file-prefix kaggle/combined/arc-agi \
  --output-dir data/arc1concept-aug-1000 \
  --subsets training evaluation concept \
  --test-set-name evaluation

# Sudoku-Extreme
python dataset/build_sudoku_dataset.py \
  --output-dir data/sudoku-extreme-1k-aug-1000 \
  --subsample-size 1000 --num-aug 1000
```

### Training Example (ARC-AGI)

```bash
torchrun --nproc-per-node 4 --rdzv_backend=c10d \
  --rdzv_endpoint=localhost:0 --nnodes=1 pretrain.py \
  arch=trm \
  data_paths="[data/arc12concept-aug-1000]" \
  arch.L_layers=2 \
  arch.H_cycles=3 arch.L_cycles=4 \
  +run_name=pretrain_att_arc12concept_4 ema=True
```

**Expected runtime:** ~3 days on 4x H-100 GPUs

---

## Research Implications

**For AI Development:**
- Challenges the "bigger is better" paradigm in AI
- Demonstrates parameter efficiency through recursive reasoning
- Opens new research directions beyond LLM scaling

**For Practitioners:**
- Achievable results without massive computational budgets
- Applicable to resource-constrained environments
- Framework for building efficient reasoning systems

**For Research Community:**
- Simplified approach enables easier experimentation
- Foundation for future recursive reasoning research
- Alternative to expensive large-scale model training

---

## Key Technical Innovations

1. **Recursive Latent Updates:** Progressive refinement through iterative latent space updates
2. **Parameter Efficiency:** 7M parameters achieving competitive results with billion-parameter models
3. **Simplicity:** Core recursive reasoning without biological or mathematical complexity
4. **Generalization:** Strong performance across multiple challenging benchmarks

---

## Citations & Credits

**Original Paper:**
```bibtex
@article{trm2024,
  title={Less is More: Recursive Reasoning with Tiny Networks},
  author={Samsung SAIL Montreal},
  journal={arXiv preprint arXiv:2510.04871},
  year={2024}
}
```

**Source Repository:** [github.com/SamsungSAILMontreal/TinyRecursiveModels](https://github.com/SamsungSAILMontreal/TinyRecursiveModels)

**Hosted for educational purposes on StartAITools.com**

---

## Explore the Research

- [View Full README](README/)
- [Paper on arXiv](https://arxiv.org/abs/2510.04871)
- [Dataset Preparation Scripts](dataset/)
- [Model Architecture](arch/)
- [Training Scripts](pretrain.py)

---

**Ready to dive deeper?** Explore the [full repository contents](README/) or jump straight to the [paper](https://arxiv.org/abs/2510.04871).
