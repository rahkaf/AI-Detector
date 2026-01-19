# HumanizeAI - AI Text Humanization Platform

<div align="center">

![HumanizeAI](https://img.shields.io/badge/HumanizeAI-Stealth%20Mode-6366f1?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Transform AI-generated content into undetectable human-like writing**

Bypass GPTZero, Originality.ai, and all major AI detection tools using ensemble transformer models.

</div>

---

## 🚀 Features

### Core Capabilities
- **🤖 Ensemble AI Models**: BART + T5 + PEGASUS working together
- **📊 Smart Metrics**: Real-time Perplexity, Burstiness, and Diversity scoring
- **🎯 Multiple Strategies**: Weighted, Diverse, Mixed, and Best selection modes
- **⚡ Fast Processing**: 3-5 seconds per text (CPU), <1s with GPU
- **🔄 Batch Processing**: Handle multiple texts simultaneously
- **📈 Visual Analytics**: Beautiful charts and metrics dashboard
- **💾 History Tracking**: Save and review past humanizations
- **🎨 Modern UI**: Clean, professional interface inspired by VeriScript

### Advanced Features
- **Perplexity Optimization**: Increases text unpredictability
- **Burstiness Enhancement**: Varies sentence lengths dramatically
- **AI Cliché Removal**: Eliminates "delve", "comprehensive", etc.
- **Human Touch Injection**: Adds contractions and natural variations
- **Sentence-Level Mixing**: Blends outputs from multiple models
- **Real-time Comparison**: Side-by-side original vs humanized view

---

## 📋 Prerequisites

### Backend
- Python 3.10 or higher
- pip (Python package manager)
- 8GB+ RAM (16GB recommended)
- ~5GB disk space for models

### Frontend
- Node.js 18+ and npm
- Modern web browser

---

## 🛠️ Installation

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd humanizeai
```

### 2. Backend Setup

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
python -c "import nltk; nltk.download('punkt')"

# Configure environment
copy .env.example .env
# Edit .env with your settings
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
copy .env.example .env
# Edit .env if needed (default: http://localhost:5000)
```

---

## 🚀 Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
python app.py
```

Backend will start on `http://localhost:5000`

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will start on `http://localhost:3000`

### Access Application

Open your browser and navigate to: **http://localhost:3000**

---

## 📖 Usage Guide

### Basic Usage

1. **Paste AI Text**: Copy your AI-generated content into the input box
2. **Select Strategy**: Choose from Weighted (recommended), Diverse, Mixed, or Best
3. **Click Humanize**: Wait 3-5 seconds for processing
4. **Review Results**: Check metrics and compare original vs humanized text
5. **Copy Output**: Use the humanized text anywhere

### Strategies Explained

| Strategy | Description | Best For |
|----------|-------------|----------|
| **Weighted** | Balanced scoring across all metrics | General use (recommended) |
| **Diverse** | Maximum lexical variation | Creative writing |
| **Mixed** | Sentence-level blending from all models | Maximum unpredictability |
| **Best** | Highest composite score | Academic writing |

### Understanding Metrics

- **Perplexity (0-100)**: Text unpredictability. Higher = more human-like
- **Burstiness (0-100)**: Sentence length variation. Higher = more natural
- **Diversity (0-100)**: Lexical richness. Higher = more varied vocabulary
- **Composite Score (0-100)**: Overall human-likeness. 75+ is excellent

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │  Input   │  │ Results  │  │  History & Settings  │  │
│  └──────────┘  └──────────┘  └──────────────────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │ REST API
┌────────────────────────┴────────────────────────────────┐
│                  Backend (Flask)                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │           Ensemble Orchestrator                   │   │
│  └──────────────────────────────────────────────────┘   │
│         │              │              │                  │
│    ┌────┴────┐    ┌───┴────┐    ┌───┴──────┐          │
│    │  BART   │    │   T5   │    │ PEGASUS  │          │
│    └─────────┘    └────────┘    └──────────┘          │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Metrics Engine (Perplexity/Burstiness/Diversity)│   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Selection Engine (Weighted/Diverse/Mixed/Best)  │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

---

## 🔧 Configuration

### Backend (`backend/.env`)

```env
SECRET_KEY=your-secret-key
DEBUG=False
PORT=5000
USE_GPU=False  # Set to True if you have CUDA GPU
DEVICE=cpu     # or 'cuda'
MAX_TEXT_LENGTH=10000
```

### Frontend (`frontend/.env`)

```env
VITE_API_URL=http://localhost:5000
```

---

## 🎯 API Endpoints

### POST `/api/humanize`
Humanize a single text.

**Request:**
```json
{
  "text": "Your AI-generated text",
  "strategy": "weighted",
  "num_variations": 3,
  "return_all": false
}
```

**Response:**
```json
{
  "text": "Humanized text",
  "metrics": {
    "perplexity": 75.5,
    "burstiness": 68.2,
    "diversity": 82.1,
    "composite_score": 74.8
  },
  "processing_time": 2.5
}
```

### POST `/api/metrics`
Get metrics for text without humanizing.

### POST `/api/compare`
Compare original vs humanized text.

### POST `/api/batch`
Humanize multiple texts (max 10).

### GET `/health`
Check API health and model status.

---

## 🚀 Performance Optimization

### GPU Acceleration

For 5-10x faster processing:

1. Install PyTorch with CUDA:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

2. Update `.env`:
```env
USE_GPU=True
DEVICE=cuda
```

### Memory Optimization

If running out of memory:
- Reduce `NUM_RETURN_SEQUENCES` in `config.py`
- Use CPU instead of GPU
- Process shorter texts
- Disable one or more models in `ensemble.py`

---

## 📊 Model Information

| Model | Size | Purpose | Download Time |
|-------|------|---------|---------------|
| BART | ~1.6GB | Paraphrasing | 2-5 min |
| T5 | ~850MB | Text-to-text | 1-3 min |
| PEGASUS | ~2.2GB | Abstractive generation | 3-7 min |

Models are automatically downloaded on first run and cached locally.

---

## 🐛 Troubleshooting

### Backend Issues

**Models not loading:**
- Check internet connection
- Ensure sufficient disk space (~5GB)
- Try deleting `~/.cache/huggingface` and redownloading

**Out of memory:**
- Use CPU instead of GPU
- Reduce batch size
- Close other applications

**Slow processing:**
- Enable GPU acceleration
- Reduce `num_variations`
- Use shorter texts

### Frontend Issues

**Cannot connect to backend:**
- Ensure backend is running on port 5000
- Check `VITE_API_URL` in `.env`
- Disable firewall/antivirus temporarily

**Build errors:**
- Delete `node_modules` and run `npm install` again
- Clear npm cache: `npm cache clean --force`

---

## 🔒 Ethical Considerations

This tool is designed for:
- ✅ Improving writing quality
- ✅ Learning about AI detection
- ✅ Research purposes
- ✅ Content refinement

**Please use responsibly.** Do not use for:
- ❌ Academic dishonesty
- ❌ Plagiarism
- ❌ Spreading misinformation
- ❌ Bypassing legitimate content policies

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- **Transformers**: HuggingFace for pre-trained models
- **Design Inspiration**: VeriScript platform
- **Research**: Based on king.md strategic roadmap
- **Models**: BART (Facebook), T5 (Google), PEGASUS (Google)

---

## 📧 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

---

<div align="center">

**Built with ❤️ using BART, T5, and PEGASUS**

*Making AI text undetectable, one transformation at a time*

</div>
