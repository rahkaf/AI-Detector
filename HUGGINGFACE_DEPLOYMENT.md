# 🚀 Hugging Face Spaces Deployment Guide

Complete guide to deploy AI Humanizer v2.0 on Hugging Face Spaces with GPU acceleration

---

## 📋 Prerequisites

- Hugging Face account (free)
- Git installed locally
- Python files uploaded to GitHub repository

---

## 🎯 Step-by-Step Deployment

### 1. Create Hugging Face Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Choose **"New Space"**
4. Fill in details:
   - **Owner**: Your username
   - **Space name**: `ai-humanizer` (or your choice)
   - **License**: MIT
   - **SDK**: Docker
   - **Docker template**: Blank (we're providing Dockerfile)
   - **Visibility**: Public or Private
5. Click **"Create Space"**

### 2. Upload Files

Upload these files to your Space (via Git):

**Required Files:**
```
backend/
├── Dockerfile
├── requirements_hf.txt
├── app_hf.py
├── .dockerignore
├── config_v2.py
├── models/
│   ├── advanced_ensemble.py
│   ├── bart_model.py
│   ├── t5_model.py
│   └── pegasus_model.py
└── utils/
    ├── advanced_metrics_v2.py
    ├── enhanced_preprocessor.py
    └── preprocessor.py
```

**Methods to upload:**

**Option A: Git Clone (Recommended)**
```bash
git clone https://huggingface.co/spaces/<YOUR_USERNAME>/<SPACE_NAME>.git
cd <SPACE_NAME>

# Copy your backend files to the cloned directory
cp -r /path/to/your/backend/* .

# Commit and push
git add .
git commit -m "Initial deploy of AI Humanizer v2.0"
git push
```

**Option B: Web Upload**
1. Go to your Space page
2. Click **"Files"** tab
3. Click **"Upload files"**
4. Upload all files listed above

### 3. Choose Hardware (GPU)

**IMPORTANT**: Select GPU for 5-6x faster processing!

1. Go to your Space **"Settings"** tab
2. Find **"Hardware"** section
3. Select one of:
   - **T4 Free** (Recommended, free)
   - **T4 Small** ($0.20/hour)
   - **V100 Small** ($0.50/hour)
   - **A100 Small** ($1.00/hour)

**GPU Comparison:**
| GPU | Memory | Speedup vs CPU | Cost |
|-----|--------|-----------------|------|
| T4 | 16GB | **5-6x** | Free |
| V100 | 16GB | **6-8x** | $0.50/hour |
| A100 | 40GB | **8-10x** | $1.00/hour |

**Recommendation**: Use **T4 Free** for testing, upgrade if you need more power.

### 4. Wait for Build

Hugging Face will automatically:
1. Build Docker image
2. Download models (~2-5GB total)
3. Install dependencies
4. Start the application

**Expected times:**
- **First build**: 10-15 minutes (model downloads)
- **Subsequent builds**: 3-5 minutes

Check the **"Logs"** tab for progress.

### 5. Test the API

Once the Space is running, test the endpoints:

**Health Check:**
```bash
curl https://<YOUR_USERNAME>-<SPACE_NAME>.hf.space/health
```

**Humanize Text (Standard):**
```bash
curl -X POST https://<YOUR_USERNAME>-<SPACE_NAME>.hf.space/api/humanize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your AI-generated text here",
    "strategy": "adaptive",
    "num_variations": 3,
    "return_all": false,
    "use_gpt2": true
  }'
```

**Humanize Text (Ultra Mode):**
```bash
curl -X POST https://<YOUR_USERNAME>-<SPACE_NAME>.hf.space/api/humanize/ultra \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your AI-generated text here",
    "strategy": "adaptive"
  }'
```

**Text Analysis:**
```bash
curl -X POST https://<YOUR_USERNAME>-<SPACE_NAME>.hf.space/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here"}'
```

---

## 🔗 Connect Frontend to Hugging Face Space

Update your frontend `.env` file:

```env
VITE_API_URL=https://<YOUR_USERNAME>-<SPACE_NAME>.hf.space
```

Then restart your frontend:

```bash
cd frontend
npm run dev
```

---

## 📊 Performance Comparison

| Mode | Local CPU | Hugging Face GPU | Speedup |
|-------|------------|-------------------|----------|
| Standard | 45-60s | 5-10s | **5-6x** |
| Ultra | 2-5min | 30-60s | **4-5x** |

**Total speedup: 5-6x faster!** 🚀

---

## ⚠️ Troubleshooting

### Build Fails

**Error: Module not found**
- Ensure all files are uploaded
- Check file structure matches requirements
- Review build logs

**Error: Out of memory**
- Reduce model complexity
- Use smaller GPU (if available)
- Check hardware requirements

### Runtime Errors

**Error: CUDA out of memory**
- Reduce batch size in config_v2.py
- Use CPU fallback
- Upgrade to larger GPU

**Error: Slow response**
- Check if GPU is active
- Review logs for bottlenecks
- Consider upgrading GPU tier

### Connection Issues

**Frontend can't connect**
- Check CORS settings (should be `*`)
- Verify URL is correct
- Check Space is running (not sleeping)
- Review firewall settings

---

## 💰 Cost Estimation

**Free Tier (T4):**
- **Cost**: $0/month
- **Requests**: Unlimited
- **Limitations**: May sleep after inactivity

**Paid Tier (Example: T4 Small):**
- **Cost**: $0.20/hour = $144/month (if running 24/7)
- **Better option**: Use Sleep after inactivity
- **Estimated**: $20-50/month for typical usage

**Recommendation**: Start with **T4 Free**, upgrade only if needed.

---

## 🎯 Best Practices

### 1. Optimize for GPU
- Use **Ultra Mode** sparingly (30-60s on GPU)
- Batch requests when possible
- Use caching to reduce redundant processing

### 2. Monitor Usage
- Check Space logs regularly
- Monitor GPU memory usage
- Track response times

### 3. Handle Errors Gracefully
- Implement retry logic in frontend
- Show user-friendly error messages
- Provide fallback strategies

### 4. Optimize Frontend
- Update API URL dynamically
- Add connection timeout handling
- Implement request queuing for high traffic

---

## 🔄 Updates and Maintenance

### Updating Your Space

```bash
# Clone your Space
git clone https://huggingface.co/spaces/<YOUR_USERNAME>/<SPACE_NAME>.git
cd <SPACE_NAME>

# Pull latest changes
git pull

# Make your changes locally

# Push updates
git add .
git commit -m "Update: description of changes"
git push
```

Space will automatically rebuild and redeploy.

---

## 📝 API Reference

### Base URL
```
https://<YOUR_USERNAME>-<SPACE_NAME>.hf.space
```

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Check API health and GPU status |
| `/api/humanize` | POST | Standard humanization |
| `/api/humanize/ultra` | POST | Ultra mode (maximum evasion) |
| `/api/metrics` | POST | Get text metrics |
| `/api/compare` | POST | Compare texts |
| `/api/batch` | POST | Batch humanization |
| `/api/analyze` | POST | Deep text analysis |
| `/api/models/info` | GET | Model information |

---

## 🔐 Security Considerations

### 1. Make Private (Optional)
- Set Space visibility to "Private"
- Only accessible via password/API key

### 2. Add Rate Limiting (Future)
- Implement rate limiting in app_hf.py
- Use Hugging Face's built-in features

### 3. Monitor Abuse
- Review logs regularly
- Track unusual usage patterns
- Implement IP blocking if needed

---

## 🎉 Success!

Your AI Humanizer v2.0 is now running on Hugging Face with GPU acceleration!

**Expected Results:**
- ⚡ **5-6x faster** processing
- ✅ **GPU acceleration** for better performance
- 🚀 **Auto-scaling** with multiple users
- 💰 **Free hosting** (with T4 GPU)
- 🌐 **Global access** via HTTPS

**Next Steps:**
1. Update frontend `.env` to point to Hugging Face URL
2. Test all endpoints
3. Monitor performance in Space logs
4. Deploy to production when ready

---

## 📞 Support

For issues or questions:
- Check Hugging Face Space documentation
- Review Space logs
- Check GitHub issues: https://github.com/rahkaf/AI-Detector/issues
- Hugging Face Community Forum

---

**Happy humanizing with GPU speed! 🚀**
