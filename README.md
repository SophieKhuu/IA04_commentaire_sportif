# Volleyball Commentary Analyzer

Analyze sports commentary with AI to generate player performance ratings.

## 🎯 Features

- **Multimodal Input**: Text & audio (transcribed with Whisper)
- **LLM-Powered Analysis**: Uses Groq API for fast inference
- **6-Criteria Scoring**: Technique, Defense, Attitude, Physique, Decision-making, Other
- **Structured Output**: JSON, CSV export
- **Streamlit UI**: User-friendly web interface
- **High Fidelity**: Prompt engineering for accurate volleyball analysis

## 📋 Requirements

- Python 3.10+
- Groq API key (free tier available at api.groq.com)
- FFmpeg (for audio transcription)

## 🚀 Quick Start

### 1. Clone & Setup

```bash
cd IA04_commentaire_sportif
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

### 2. Configure

Create `.env` file (copy from `.env.example`):

```bash
GROQ_API_KEY=your_api_key_here
FFMPEG_PATH=c:\path\to\ffmpeg\bin  # Windows path to ffmpeg-essentials_build/bin
```

### 3. Run

```bash
streamlit run main.py
```

Visit: `http://localhost:8501`

## 📊 Usage

### Text Analysis

1. Paste commentary in text area
2. Click **Analyze**
3. View player ratings and export results

### Audio Analysis

1. Upload MP3/WAV/M4A file
2. Wait for transcription
3. Click **Analyze**
4. View results

## 📁 Project Structure

```
src/
├── config.py              # Configuration & constants
├── models/
│   └── schemas.py         # Pydantic models
├── pipeline/
│   ├── llm_client.py      # Groq wrapper
│   ├── extractor.py       # JSON extraction
│   ├── scorer.py          # Score calculation
│   ├── transcriber.py     # Whisper wrapper
│   └── text_processor.py  # Text cleaning
└── ui/
    └── app.py             # Streamlit main app

tests/                      # Unit tests
data/                       # Sample data
docs/                       # Documentation
```

## 🔧 Configuration

### Scoring Weights

Adjust criterion weights in sidebar:
- Technique (default 20%)
- Defense (default 25%)
- Attitude (default 20%)
- Physique (default 15%)
- Decision Tactique (default 15%)
- Other (default 5%)

### LLM Settings

Edit `.env`:
- `LLM_MODEL`: Model name (default: mixtral-8x7b-32768)
- `LLM_TEMPERATURE`: Sampling temperature (0-1, default: 0.3)
- `LLM_MAX_TOKENS`: Max response length (default: 2048)

## 📤 Export

Results can be exported as:
- **CSV**: Tabular format with all player scores
- **JSON**: Complete analysis with metadata

## 🧪 Testing

```bash
pytest tests/ -v
pytest tests/ --cov=src  # With coverage
```

## 🎓 Sample Data

Try with example commentaries in `data/sample_commentaries.json`

## 🐳 Docker (Optional)

```bash
docker build -t volleyball-analyzer .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key volleyball-analyzer
```

## 📚 Prompt Engineering

Key prompt located in `src/config.py`:
- System prompt: `SYSTEM_PROMPT_VOLLEYBALL`
- Customize for specific needs

For tuning, see `docs/PROMPT_ENGINEERING.md`

## ⚠️ Limitations

- Requires internet for Groq API
- Whisper model download on first use (~1.5 GB for 'base')
- Audio transcription quality depends on audio clarity

## 🔄 Future Improvements

- [ ] User authentication + history persistence
- [ ] Database backend (PostgreSQL)
- [ ] Player performance trends
- [ ] Manual score correction UI
- [ ] Batch processing
- [ ] Multi-language support
- [ ] Custom model fine-tuning

## 📖 Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Prompt Engineering](docs/PROMPT_ENGINEERING.md)

## 📝 License

Project for IA04 course

## 👤 Author

IA04 Team

---

**Questions?** Check the documentation or run tests to verify setup.
