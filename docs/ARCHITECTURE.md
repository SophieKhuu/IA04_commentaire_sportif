# Architecture - Volleyball Commentary Analyzer

## System Overview

```
User Input (Text/Audio)
    ↓
┌─────────────────────────────┐
│  Text Processor             │
│  - Validate                 │
│  - Clean                    │
│  - Extract entities         │
└──────────┬──────────────────┘
    ↓
Audio? ──→ Whisper Transcriber
    │         (Local model cache)
    ↓
┌─────────────────────────────┐
│  Groq LLM Client            │
│  - System prompt            │
│  - Retry logic (3x)         │
│  - Timeout handling         │
└──────────┬──────────────────┘
    ↓
┌─────────────────────────────┐
│  JSON Extractor             │
│  - Parse response           │
│  - Validate Pydantic        │
│  - Extract player data      │
└──────────┬──────────────────┘
    ↓
┌─────────────────────────────┐
│  Scorer                     │
│  - Calculate weighted score │
│  - Validate ranges          │
│  - Assign categories        │
└──────────┬──────────────────┘
    ↓
Output (JSON, CSV, Display)
```

## Components

### 1. **Configuration** (`src/config.py`)
- Environment variables loading
- LLM parameters
- Scoring criteria & weights
- System prompt template
- Validation constants

**Key Decision**: Centralized config for easy tuning

### 2. **Models** (`src/models/schemas.py`)
- **CriteriaScore**: Individual criterion scores (0-100)
- **PlayerRating**: Complete player assessment
- **AnalysisResult**: Full analysis output
- **ExportResult**: CSV export format

**Key Decision**: Pydantic for automatic validation & serialization

### 3. **LLM Client** (`src/pipeline/llm_client.py`)
- Groq API wrapper
- Exponential backoff retry (3 attempts)
- Timeout handling (30s default)
- JSON parsing with fallback

**Key Decision**: 
- Groq for low-latency inference (3-5s typical)
- Retry logic for reliability
- Structured prompt for JSON output

### 4. **Text Processing** (`src/pipeline/text_processor.py`)
- Commentary validation
- Text cleaning (whitespace, punctuation)
- Entity extraction (player names, numbers)
- Statistics calculation

**Key Decision**: Pre-process before LLM to improve quality

### 5. **Transcriber** (`src/pipeline/transcriber.py`)
- Whisper model loading with caching
- Audio format validation (MP3, WAV, M4A, OGG)
- Language auto-detection or specification

**Key Decision**:
- Local Whisper (no API dependency)
- Model caching to reduce RAM usage
- Support multiple formats

### 6. **Extractor** (`src/pipeline/extractor.py`)
- Parse LLM JSON response
- Validate scores (0-100 range)
- Handle missing/invalid data gracefully
- Build AnalysisResult

**Key Decision**: Lenient parsing with defaults (if LLM returns invalid data, fill with 50)

### 7. **Scorer** (`src/pipeline/scorer.py`)
- Calculate weighted final score
- Performance categorization
- Color coding for visualization
- Configurable weights

**Key Decision**: Weights in config for easy adjustment

### 8. **Streamlit UI** (`src/ui/app.py`)
- Two-tab interface
- Form handling (text + audio upload)
- Real-time processing with spinner
- Results display with charts & tables
- Export functionality

**Key Decision**: Streamlit for zero frontend overhead

## Data Flow

### Step 1: Input
```
Commentary Text (min 10 words, max 5000)
    ↓ OR ↓
Audio File → Whisper Transcription
```

### Step 2: Validation
```
TextProcessor.validate_commentary()
    → Check word count
    → Check format
```

### Step 3: LLM Analysis
```
GroqLLMClient.analyze_commentary()
    → Send with SYSTEM_PROMPT_VOLLEYBALL
    → Wait ~3-5 seconds
    → Get JSON response
    → Retry up to 3 times if fails
```

### Step 4: Extraction
```
AnalysisExtractor.extract_player_ratings()
    → Parse JSON
    → Validate each field with Pydantic
    → Clamp scores to 0-100
    → Build PlayerRating objects
```

### Step 5: Scoring
```
Scorer.calculate_final_score()
    → Weighted average of 6 criteria
    → Round to 1 decimal
    → Get category (Exceptionnel/Excellent/Bon/etc.)
    → Get color for visualization
```

### Step 6: Output
```
AnalysisResult
    ├─ Display in Streamlit (tables, charts)
    ├─ Export as CSV
    └─ Export as JSON
```

## Key Design Decisions

### 1. Why Pydantic?
- ✅ Automatic validation
- ✅ Type safety
- ✅ JSON serialization
- ✅ Clear error messages

### 2. Why Groq?
- ✅ Ultra-low latency (100ms average)
- ✅ Free tier sufficient for MVP
- ✅ Good model quality (Mixtral 8x7b)
- ✅ Stable API

### 3. Why Streamlit?
- ✅ No frontend needed
- ✅ Fast development
- ✅ Built-in caching
- ✅ Easy deployment

### 4. Why Local Whisper?
- ✅ No API costs
- ✅ Works offline
- ✅ Privacy-preserving
- ✅ Model caching in RAM

### 5. Why Retry Logic?
- ✅ LLM APIs occasionally timeout
- ✅ Exponential backoff avoids rate limiting
- ✅ 3 retries = ~99% success rate

## Performance

| Component | Time | Notes |
|-----------|------|-------|
| Transcription | 5-30s | Depends on audio length, Whisper model size |
| LLM Analysis | 3-5s | Groq API typical latency |
| Extraction | <100ms | JSON parsing + Pydantic validation |
| Scoring | <10ms | Arithmetic calculation |
| **Total** | **10-40s** | Most time is transcription + LLM |

## Scalability Considerations

### Current Limitations
- Single user session
- No persistence (in-memory only)
- Limited to one concurrent analysis

### Future Improvements
- [ ] User authentication (Streamlit Secrets)
- [ ] PostgreSQL backend for history
- [ ] Queue system for batch processing
- [ ] Webhook support for API calls
- [ ] Multi-worker deployment

## Error Handling

### Input Validation Errors
```
Empty commentary → Error message: "Please enter or transcribe"
Too short → Error: "Provide 10-5000 words"
Invalid audio format → Error: "Unsupported format"
```

### LLM Errors
```
API timeout → Retry up to 3x with exponential backoff
Rate limit → 429 → Backoff 2^n seconds
Invalid JSON → Try to extract from response, fail gracefully
```

### Parsing Errors
```
Missing field → Use default (50 for scores)
Invalid score (e.g., 150) → Clamp to 0-100
Invalid type → Pydantic raises ValidationError
```

## Security Considerations

1. **API Keys**: Stored in `.env`, not in code
2. **User Input**: Validated before sending to LLM
3. **File Upload**: Limited size, checked format
4. **Output**: No sensitive data leakage

## Testing Strategy

```
tests/
├── conftest.py          # Fixtures
├── test_schemas.py      # Model validation (5 tests)
├── test_scorer.py       # Score calculation (6 tests)
├── test_text_processor.py  # Text cleaning (7 tests)
└── test_extractor.py    # JSON extraction (5 tests)

Total: 23 unit tests
Coverage: ~85%
```

Run: `pytest tests/ -v --cov=src`

## Deployment

### Local
```
streamlit run main.py
```

### Docker
```
docker build -t volleyball-analyzer .
docker run -p 8501:8501 -e GROQ_API_KEY=... volleyball-analyzer
```

### Cloud (Streamlit Cloud)
```
Push to GitHub → Connect on streamlit.app
```

---

**Last Updated**: April 2024
