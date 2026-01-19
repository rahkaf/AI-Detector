# 🚀 Advanced AI Humanization System v2.0

<div align="center">

![Version](https://img.shields.io/badge/Version-2.0%20Advanced-6366f1?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Advanced AI Detection Evasion System - Bypass Originality.ai & GPTZero**

Next-generation ensemble AI humanizer with sophisticated blending, adaptive strategies, and multi-pass refinement

</div>

---

## 🎯 What's New in v2.0

### 🏆 Major Upgrades

**Advanced Ensemble System**
- ✅ Adaptive strategy selection based on text analysis
- ✅ Cascade blending through multiple models
- ✅ Style transfer with configurable templates
- ✅ Intelligent sentence-level blending with quality scoring
- ✅ Multi-pass recursive refinement with quality gates

**Enhanced Metrics Engine**
- ✅ GPT-2 based true perplexity calculation with caching
- ✅ Advanced n-gram entropy (2-gram, 3-gram, 4-gram analysis)
- ✅ Enhanced burstiness with skewness calculation
- ✅ Type-Token Ratio (TTR) for vocabulary richness
- ✅ Comprehensive stylometric features analysis

**Sophisticated Preprocessing**
- ✅ Syntactic restructuring to break AI patterns
- ✅ Dramatic burstiness enhancement
- ✅ Context-aware phrase variations
- ✅ Advanced linguistic noise injection
- ✅ Intelligent sentence opening variation
- ✅ Expanded AI cliché detection (50+ patterns)

**New Processing Modes**
- ✅ **Standard Mode**: Fast (30-60s), good evasion
- ✅ **Ultra Mode**: Maximum evasion (2-5 min), multi-stage enhancement

**New Strategies**
- ✅ **Adaptive**: Auto-selects optimal strategy
- ✅ **Cascade**: Pass outputs through multiple models
- ✅ **Style Transfer**: Applies style matching transformations
- ✅ **Mixed**: Combines multiple strategies

---

## 📊 Detection Capabilities

### Supported AI Detectors

| Detector | Basic Mode | Ultra Mode | Notes |
|-----------|-------------|-------------|---------|
| **Quillbot** | ✅ Excellent | ✅ Perfect | Easily bypassed |
| **Scribbr** | ✅ Excellent | ✅ Perfect | Easily bypassed |
| **Originality.ai** | ⚠️ Moderate | ✅ Good | Ultra mode recommended |
| **GPTZero** | ⚠️ Moderate | ✅ Good | Ultra mode recommended |
| **Turnitin** | ⚠️ Difficult | ✅ Moderate | Challenging |
| **Copyleaks** | ⚠️ Moderate | ✅ Good | Mixed results |

### Performance Metrics

**Target Scores (Higher = Better):**
- **Composite Score**: 85+ (Ultra), 75+ (Standard)
- **Perplexity**: 60+ (unpredictability)
- **Burstiness**: 70+ (sentence variation)
- **Detection Resistance**: VERY HIGH (Ultra), HIGH (Standard)

---

## 🛠️ Installation

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

# Configure environment
copy .env.example .env
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
copy .env.example .env
# Edit .env if needed (default: http://localhost:5000)
```

---

## 🚀 Usage

### Start Backend (Advanced Mode)

```bash
cd backend
venv\Scripts\activate  # Windows
python app_v2.py
```

Backend will start on `http://localhost:5000`

### Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will start on `http://localhost:3000`

---

## 📖 API Endpoints

### POST `/api/humanize` (Standard Mode)

Humanize text with standard processing (30-60 seconds).

**Request:**
```json
{
  "text": "Your AI-generated text",
  "strategy": "adaptive",
  "num_variations": 3,
  "return_all": false,
  "use_gpt2": true
}
```

**Strategies Available:**
- `adaptive` - Auto-selects optimal strategy (recommended)
- `cascade` - Pass outputs through multiple models
- `style_transfer` - Applies style matching
- `mixed` - Combines multiple strategies
- `weighted`, `diverse`, `best` - Classic strategies

**Response:**
```json
{
  "text": "Humanized text",
  "original_text": "Original text",
  "metrics": {
    "perplexity": 72.5,
    "burstiness": 68.2,
    "bigram_entropy": 75.1,
    "trigram_entropy": 70.3,
    "pos_entropy": 65.8,
    "semantic_coherence": 62.5,
    "composite_score": 78.5,
    "detection_resistance": "HIGH"
  },
  "strategy": "adaptive",
  "processing_time": 45.2
}
```

### POST `/api/humanize/ultra` (Ultra Mode)

Maximum detection evasion with multi-stage enhancement (2-5 minutes).

**Request:**
```json
{
  "text": "Your AI-generated text",
  "strategy": "adaptive"
}
```

**Response:**
```json
{
  "text": "Ultra humanized text",
  "metrics": {
    "composite_score": 88.5,
    "detection_resistance": "VERY HIGH"
  },
  "mode": "ultra",
  "iterations": 5,
  "description": "Maximum detection evasion with multi-stage enhancement"
}
```

### POST `/api/analyze`

Deep text analysis with optimization recommendations.

**Request:**
```json
{
  "text": "Text to analyze"
}
```

**Response:**
```json
{
  "text_analysis": {
    "word_count": 150,
    "vocabulary_diversity": 0.65,
    "category": "academic"
  },
  "metrics": { ... },
  "recommendations": [
    "Increase vocabulary diversity",
    "Optimal strategy: cascade"
  ],
  "detection_risk": "MEDIUM"
}
```

### POST `/api/compare`

Compare original vs humanized text.

### POST `/api/batch`

Batch humanize multiple texts (max 10).

### GET `/api/models/info`

Get model information and capabilities.

---

## 🔧 Configuration

### Advanced Settings (`backend/.env`)

```env
# Device
USE_GPU=True
DEVICE=cuda

# Generation parameters (Ultra mode)
ULTRA_TEMPERATURE=2.5
ULTRA_TOP_K=250
ULTRA_TOP_P=0.995
ULTRA_NUM_VARIATIONS=5

# Quality gates
TARGET_SCORE=85.0
MAX_ITERATIONS=5

# GPT-2 for perplexity
ENABLE_GPT2_CACHE=True
```

---

## 📈 Performance Optimization

### Speed Improvements

**Standard Mode:**
- CPU: 45-60 seconds
- GPU: 5-10 seconds

**Ultra Mode:**
- CPU: 3-5 minutes
- GPU: 30-60 seconds

### Memory Optimization

- GPT-2 model caching enabled
- Metrics calculation caching (LRU cache, 1000 entries)
- Lazy model loading
- Optimized batch processing

---

## 🎯 Best Practices

### For Maximum Detection Evasion

1. **Use Ultra Mode** for critical texts
2. **Select Adaptive Strategy** for auto-optimization
3. **Choose Cascade** for multi-model processing
4. **Review Recommendations** from analysis endpoint
5. **Apply Multiple Iterations** if score < 85

### Text Quality Tips

- ✅ Vary sentence lengths dramatically
- ✅ Use diverse vocabulary
- ✅ Avoid AI clichés (delve, comprehensive, etc.)
- ✅ Add conversational elements occasionally
- ✅ Mix short and long sentences

---

## 🔬 Technical Details

### Ensemble Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Advanced Ensemble System v2.0                │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────┐  │
│  │        Adaptive Strategy Selection Engine          │  │
│  │  - Text Analysis (Category, Diversity)          │  │
│  │  - Parameter Optimization (Temp, Top-K, Top-P)  │  │
│  └───────────────────────────────────────────────────┘  │
│                        ↓                                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │     Multi-Model Generation Pipeline              │  │
│  │  ┌─────┐  ┌─────┐  ┌──────┐          │  │
│  │  │ BART│  │ T5  │  │PEGASUS│          │  │
│  │  └─────┘  └─────┘  └──────┘          │  │
│  └───────────────────────────────────────────────────┘  │
│                        ↓                                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │     Advanced Blending Strategies               │  │
│  │  - Cascade (model-to-model)                │  │
│  │  - Intelligent sentence blending            │  │
│  │  - Style transfer with templates           │  │
│  └───────────────────────────────────────────────────┘  │
│                        ↓                                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │   Enhanced Preprocessing Pipeline               │  │
│  │  - Syntactic restructuring                 │  │
│  │  - Burstiness enhancement                 │  │
│  │  - Linguistic noise injection               │  │
│  │  - AI cliché removal (50+ patterns)    │  │
│  └───────────────────────────────────────────────────┘  │
│                        ↓                                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │   Iterative Refinement (5 max passes)      │  │
│  │   - Quality gate: 85+ composite score        │  │
│  │   - GPT-2 perplexity calculation           │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Metrics Scoring Weights

- **Perplexity**: 22% (GPT-2 based, most accurate)
- **Burstiness**: 20% (sentence variation)
- **Bigram Entropy**: 12% (2-gram diversity)
- **Trigram Entropy**: 10% (3-gram diversity)
- **POS Entropy**: 10% (part-of-speech diversity)
- **Coherence**: 8% (reduced for human-like quality)
- **Type-Token Ratio**: 10% (vocabulary richness)
- **Repetition**: 8% (penalize repetitive patterns)

---

## 🆚 v2.0 vs v1.0

| Feature | v1.0 | v2.0 |
|---------|--------|--------|
| Strategies | 4 | 7 |
| Modes | 1 | 2 (Standard + Ultra) |
| GPT-2 Perplexity | ❌ | ✅ Cached |
| Adaptive Selection | ❌ | ✅ Automatic |
| Cascade Blending | ❌ | ✅ Multi-pass |
| Style Transfer | ❌ | ✅ Templates |
| AI Clichés | ~20 | 50+ |
| Preprocessing Stages | Basic | 7-stage |
| Refinement Iterations | 3 | 5 |
| Detection Evasion | Quillbot, Scribbr | Originality.ai, GPTZero |

---

## 🐛 Troubleshooting

### Ultra Mode Issues

**Too slow:**
- Use GPU acceleration
- Reduce ULTRA_NUM_VARIATIONS to 3
- Check GPT-2 caching is enabled

**Memory errors:**
- Use CPU instead of GPU
- Reduce batch size
- Close other applications

### Quality Issues

**Score too low:**
- Try different strategies
- Use Ultra Mode
- Review analysis recommendations
- Split long text into chunks

---

## 🔒 Ethical Considerations

This tool is designed for:
- ✅ Improving writing quality
- ✅ Learning about AI detection
- ✅ Research purposes
- ✅ Content refinement

**Use responsibly:**
- ❌ Academic dishonesty
- ❌ Plagiarism
- ❌ Misinformation
- ❌ Bypassing legitimate content policies

---

## 📝 License

MIT License - See LICENSE file for details

---

<div align="center">

**Advanced AI Humanization System v2.0**

*Making AI text undetectable with sophisticated ensemble methods*

Built with ❤️ by Xargham | BeeNeural Pvt Ltd

</div>
