# MarketAI Suite - Quick Reference Guide

## 🚀 Getting Started (2 minutes)

### 1. Start the App
```bash
cd c:\Users\VAMSHI\OneDrive\Desktop\MarketMind
python app.py
```

### 2. Open Browser
Go to: **http://127.0.0.1:5000**

### 3. Start Using
- Home page shows all features
- Click any feature card to get started

---

## 🎯 Feature Quick Start

### Campaign Generator
**What it does**: Creates data-driven marketing campaigns  
**Inputs**: Product, Audience, Platform  
**Output**: Complete campaign strategy with CTAs

**Example**:
- Product: "AI email marketing platform"
- Audience: "Marketing managers at e-commerce companies"
- Platform: "LinkedIn, Instagram"

### Sales Pitch Creator
**What it does**: Crafts personalized sales pitches  
**Inputs**: Product name, Customer persona  
**Output**: 30-sec pitch, value prop, differentiators

**Example**:
- Product: "Cloud inventory system"
- Persona: "Ops director at Fortune 500 retailer"

### Lead Qualifier
**What it does**: Scores and prioritizes leads  
**Inputs**: Name, Budget, Need, Urgency  
**Output**: Score (0-100), probability, next actions

**Example**:
- Name: "Sarah Johnson"
- Budget: "$150k annual"
- Need: "Improve retention by 20%"
- Urgency: "Board needs solution by Q3"

---

## 📋 Score Scale

| Score | Category | Action |
|-------|----------|--------|
| 90-100 | 🔥 Hot | Immediate follow-up |
| 75-89 | 🟠 Warm | Priority follow-up |
| 60-74 | 🟡 Lukewarm | Nurture |
| < 60 | 🔵 Cold | Defer/Disqualify |

---

## 🔧 System Requirements

- Python 3.8+
- Groq API Key (free at groq.com)
- Flask 3.0.0
- Modern web browser

---

## 📂 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application |
| `backend/ai_engine.py` | Groq API integration |
| `backend/prompts.py` | AI prompt templates |
| `.env` | API key storage |
| `README.md` | Full documentation |
| `CONFIG.md` | Configuration guide |

---

## 🔑 Environment Setup

### Create .env File
```env
GROQ_API_KEY=your_api_key_here
```

### Get API Key
1. Visit https://console.groq.com
2. Sign up/login
3. Create API key in settings
4. Copy and paste into .env

---

## 🌐 URLs

| Page | URL |
|------|-----|
| Home | http://127.0.0.1:5000/ |
| Campaign | http://127.0.0.1:5000/campaign |
| Pitch | http://127.0.0.1:5000/pitch |
| Lead Score | http://127.0.0.1:5000/lead-score |

---

## 🐛 Quick Troubleshooting

### App won't start
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port 5000 in use
Edit `app.py`:
```python
app.run(port=5001)  # Change to 5001
```

### API key not working
- Verify `.env` file exists
- Check API key is correct
- Ensure API key not expired

---

## 📚 Documentation Files

- **README.md** - Complete documentation
- **CONFIG.md** - Configuration details
- **COMPLETION_SUMMARY.md** - What was built
- **This file** - Quick reference

---

## ✨ Features

✅ Beautiful responsive UI  
✅ Purple gradient theme  
✅ AI-powered generation  
✅ Real-time processing  
✅ Mobile friendly  
✅ Error handling  
✅ Loading indicators  
✅ Result formatting  

---

## 🎓 Platform Support

Supports marketing campaigns for:
- LinkedIn
- Facebook
- Instagram
- Twitter/X
- YouTube
- Email
- TikTok
- WhatsApp

---

## 💡 Pro Tips

1. **Detailed inputs = Better outputs**  
   More specific product/audience = better campaigns

2. **Test API key first**  
   Generate a campaign to verify API works

3. **Copy results**  
   Use browser copy/paste for generated content

4. **Save responses**  
   Keep important campaigns/pitches saved

5. **Refine prompts**  
   Edit prompts.py to customize AI behavior

---

## 📞 Help & Support

**Documentation**: See README.md  
**Configuration**: See CONFIG.md  
**What was built**: See COMPLETION_SUMMARY.md  
**Groq docs**: https://console.groq.com/docs  
**Flask docs**: https://flask.palletsprojects.com  

---

## 🎉 You're Ready!

Everything is set up and working. Start the app and begin generating marketing campaigns, sales pitches, and qualifying leads with AI power!

**Happy Marketing! 🚀**

---

**Version**: 1.0.0 | **Date**: Jan 30, 2026 | **Status**: ✅ Ready to Use