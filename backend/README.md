# HumanizeAI Backend

Python Flask backend with ensemble transformer models for text humanization.

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download NLTK Data (First Time Only)

```python
python -c "import nltk; nltk.download('punkt')"
```

### 5. Configure Environment

```bash
copy .env.example .env
```

Edit `.env` and set your configuration.

### 6. Run Server

```bash
python app.py
```

Server will start on `http://localhost:5000`

## API Endpoints

### POST /api/humanize
Humanize a single text.

**Request:**
```json
{
  "text": "Your AI-generated text here",
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
  "model": "bart",
  "processing_time": 2.5
}
```

### POST /api/metrics
Get metrics for a text.

**Request:**
```json
{
  "text": "Text to analyze"
}
```

### POST /api/compare
Compare original vs humanized text.

**Request:**
```json
{
  "original": "Original text",
  "humanized": "Humanized text"
}
```

### POST /api/batch
Humanize multiple texts.

**Request:**
```json
{
  "texts": ["text1", "text2"],
  "strategy": "weighted"
}
```

## Strategies

- **weighted**: Weighted voting based on metrics (recommended)
- **diverse**: Select most diverse output
- **mixed**: Mix sentences from different models
- **best**: Simply pick highest scoring output

## GPU Support

To use GPU acceleration:

1. Install PyTorch with CUDA support
2. Set `USE_GPU=True` in `.env`

## Model Downloads

Models are automatically downloaded on first run:
- BART: ~1.6GB
- T5: ~850MB
- PEGASUS: ~2.2GB

Total: ~4.7GB disk space required.

## Performance

- CPU: ~3-5 seconds per text
- GPU: ~0.5-1 second per text

## Troubleshooting

**Out of Memory:**
- Reduce `NUM_RETURN_SEQUENCES` in config.py
- Use CPU instead of GPU
- Process shorter texts

**Models not loading:**
- Check internet connection
- Ensure sufficient disk space
- Try deleting `~/.cache/huggingface` and redownloading
