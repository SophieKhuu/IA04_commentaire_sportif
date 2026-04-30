# 🚀 Quick Start Guide

## ✅ Project Status
**Implementation Complete** - Ready for deployment!

---

## 📋 Setup Instructions

### **Step 1: Get API Key**
1. Visit: https://console.groq.com
2. Sign up (free account)
3. Copy your API key

### **Step 2: Install Dependencies**

**Windows:**
```bash
cd c:YOUR\PATH\IA04_commentaire_sportif
install.bat
```

**Linux/Mac:**
```bash
cd ~/IA04_commentaire_sportif
bash install.sh
```

**Manual:**
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate    # Linux/Mac
pip install -r requirements.txt
```

### **Step 3: Configure API Key**

1. Open `.env` file
2. Find: `GROQ_API_KEY=your_groq_api_key_here`
3. Replace with your actual key:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here
   ```

### **Step 4: Run Application**

```bash
streamlit run main.py
```

**Opens at:** `http://localhost:8501`

---

## 🎮 Using the Application

### **Analyzing Text**
1. Go to "📝 Analysis" tab
2. Paste volleyball commentary in the text area
3. Click "🚀 Analyze"
4. View results: tables, charts, player scores
5. Download CSV or JSON

### **Analyzing Audio**
1. Go to "📝 Analysis" tab
2. Upload MP3/WAV/M4A file
3. Wait for transcription (5-30 seconds)
4. Click "🚀 Analyze"
5. View results

### **Viewing History**
1. Go to "📜 History" tab
2. See all previous analyses
3. Expand to view details

### **Configuring Scoring**
1. Open sidebar (left menu)
2. Adjust criterion weights with sliders
3. Changes apply immediately

---

## 📊 What Gets Analyzed

The system extracts and scores:

| Criterion | Definition |
|-----------|-----------|
| **Technique** | Passing accuracy, spike quality, ball control |
| **Defense** | Blocking, receiving, positioning |
| **Attitude** | Mental engagement, communication, leadership |
| **Physique** | Physical performance, explosivity, endurance |
| **Decision Tactique** | Game reading, tactical decisions |
| **Autre** | Other relevant observations |

**Final Score:** Weighted average of all 6 criteria (0-100)

---

## 📤 Export Options

### CSV Format
- Tabular: Player, Number, All Criteria, Final Score, Category
- Importable to Excel
- Download button in results

### JSON Format
- Complete analysis data
- Includes: Summary, timestamps, metadata
- Full player details

---

## 🧪 Testing

### Quick Validation
```bash
python test_quick.py
```

### Run All Tests
```bash
pytest tests/ -v
```

### With Coverage
```bash
pytest tests/ --cov=src
```

---

## 📁 Sample Data

Try these commentaries in `data/sample_commentaries.json`:

1. **France vs Argentina** (French)
   - Multiple players mentioned
   - Various criteria highlighted

2. **Training Session** (English)
   - Team-focused analysis
   - Mixed performance levels

3. **Women's Match** (French)
   - Different player names
   - Various performance levels

---

## ⚙️ Configuration Options

Edit `.env` for:

```ini
# LLM Settings
LLM_TEMPERATURE=0.3             # Lower = more deterministic
LLM_MAX_TOKENS=2048             # Response length

# Audio
WHISPER_MODEL=base              # Options: tiny, base, small, medium
WHISPER_DEVICE=cpu              # Options: cpu, cuda (GPU)

# FFmpeg (for audio download from YouTube)
FFMPEG_PATH=path/to/ffmpeg/bin
```

---

## 🎓 Example Workflow

### Text Analysis
```
"Dupont a réalisé une performance exceptionnelle en défense 
avec de nombreux blocs décisifs. Martin a montré une grande 
maîtrise technique avec ses passes précises."

↓ (Click Analyze)

Results:
- Dupont: 82/100 (Excellent)
- Martin: 78/100 (Bon)
- Team Summary: Good defensive performance
```

### Audio Analysis
```
Upload: match_highlights.mp3

↓ (Transcription: 10-20 seconds)

"Les commentateurs disent que..."

↓ (Click Analyze)

Results: Same as above
```

---

## 🔧 Troubleshooting

### **"GROQ_API_KEY not configured"**
- Edit `.env`
- Add your actual API key
- Restart app

### **"ffmpeg not found"**
- Set FFMPEG_PATH in .env
- Or install FFmpeg globally

### **"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

### **Slow transcription**
- Use `WHISPER_MODEL=tiny` (faster, less accurate)
- Or `WHISPER_DEVICE=cuda` if you have GPU

### **Timeout errors**
- Try again (retry logic built in)
- Check internet connection
- Verify Groq API status

---

## 📚 Documentation

- **README.md** - Features, installation, usage
- **ARCHITECTURE.md** - System design, components
- **PROMPT_ENGINEERING.md** - Tuning the AI prompts
- **IMPLEMENTATION_SUMMARY.md** - Technical overview

---

## 💡 Tips

1. **Better Results:**
   - Use specific player names (not just "he/she")
   - Mention specific actions (passes, blocks, errors)
   - Include context (match situation, score)

2. **Performance:**
   - Text analysis is faster than audio
   - Cache is used for repeated commentaries
   - Adjust weights to match your preferences

3. **Accuracy:**
   - Model works best with clear commentary
   - Structured commentary → better results
   - Review and adjust scores if needed

---

## 🎉 You're Ready!

```bash
streamlit run main.py
```

**Then:**
1. Open browser at http://localhost:8501
2. Paste a volleyball commentary
3. Click "Analyze"
4. See the magic! ✨

---

## 📞 Need Help?

- Check **README.md** for detailed docs
- Review **ARCHITECTURE.md** for technical details
- See **docs/PROMPT_ENGINEERING.md** for tuning tips
- Run **pytest tests/ -v** to verify setup

---

**Happy analyzing! 🏐**

Questions? Start with README.md!
