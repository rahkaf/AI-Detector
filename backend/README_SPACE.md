# 🤗 Hugging Face Space Configuration

title: AI Humanizer v2.0
emoji: 🤖
colorFrom: indigo
sdk: docker
pinned: false
license: mit
app_port: 7860

# Hugging Face Space Configuration
# 
# This Space hosts the Advanced AI Humanizer v2.0
# with GPU acceleration for fast processing

---

## 🚀 Features

- ✅ **Ultra Mode**: 30-60s (vs 2-5min on CPU)
- ✅ **Standard Mode**: 5-10s (vs 45-60s on CPU)
- ✅ **GPU Acceleration**: Uses Hugging Face free GPUs
- ✅ **API Compatible**: REST API for frontend
- ✅ **Multiple Strategies**: Adaptive, Cascade, Style Transfer
- ✅ **GPT-2 Perplexity**: Accurate detection metrics

---

## 🔧 Setup

1. Create a new Hugging Face Space
2. Choose "Docker" runtime
3. Upload these files:
   - Dockerfile
   - requirements_hf.txt
   - app_hf.py
   - .env (optional)
4. Deploy!

---

## 📊 Performance

| Mode | CPU (Local) | GPU (Hugging Face) |
|-------|-------------|---------------------|
| Standard | 45-60s | 5-10s |
| Ultra | 2-5min | 30-60s |

**Speedup: 5-6x faster!** 🚀
