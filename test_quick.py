"""
Quick test to verify all imports and basic functionality
Run this after: pip install -r requirements.txt
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Test all module imports"""
    print("🔍 Testing imports...")
    
    try:
        from src.config import (
            GROQ_API_KEY,
            LLM_MODEL,
            SCORING_CRITERIA,
            SYSTEM_PROMPT_VOLLEYBALL,
        )
        print("  ✅ src.config")
        
        from src.models.schemas import (
            CriteriaScore,
            PlayerRating,
            AnalysisResult,
        )
        print("  ✅ src.models.schemas")
        
        from src.pipeline.llm_client import GroqLLMClient
        print("  ✅ src.pipeline.llm_client")
        
        from src.pipeline.extractor import AnalysisExtractor
        print("  ✅ src.pipeline.extractor")
        
        from src.pipeline.scorer import Scorer
        print("  ✅ src.pipeline.scorer")
        
        from src.pipeline.text_processor import TextProcessor
        print("  ✅ src.pipeline.text_processor")
        
        from src.pipeline.transcriber import WhisperTranscriber
        print("  ✅ src.pipeline.transcriber")
        
        print("\n✅ All imports successful!\n")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False


def test_basic_validation():
    """Test basic model validation"""
    print("🧪 Testing model validation...")
    
    try:
        from src.models.schemas import CriteriaScore
        
        # Valid score
        score = CriteriaScore(
            technique=75,
            defense=80,
            attitude=85,
            physique=78,
            decision_tactique=72,
            autre=70,
        )
        print("  ✅ Valid CriteriaScore creation")
        
        # Invalid score should raise error
        try:
            bad_score = CriteriaScore(
                technique=150,  # Invalid
                defense=80,
                attitude=85,
                physique=78,
                decision_tactique=72,
                autre=70,
            )
            print("  ❌ Invalid score validation failed")
            return False
        except ValueError:
            print("  ✅ Invalid score correctly rejected")
        
        print("\n✅ Model validation tests passed!\n")
        return True
        
    except Exception as e:
        print(f"❌ Validation error: {str(e)}")
        return False


def test_text_processor():
    """Test text processing"""
    print("🧪 Testing text processor...")
    
    try:
        from src.pipeline.text_processor import TextProcessor
        
        # Valid commentary
        text = "This is a valid volleyball commentary with many words about player performance metrics."
        if TextProcessor.validate_commentary(text):
            print("  ✅ Valid commentary accepted")
        else:
            print("  ❌ Valid commentary rejected")
            return False
        
        # Invalid commentary
        if not TextProcessor.validate_commentary("Too short"):
            print("  ✅ Invalid commentary rejected")
        else:
            print("  ❌ Invalid commentary accepted")
            return False
        
        # Text cleaning
        dirty = "  Hello   world  !!!  "
        clean = TextProcessor.clean_text(dirty)
        if clean == "Hello world !":
            print("  ✅ Text cleaning works")
        else:
            print(f"  ⚠️  Text cleaning result: '{clean}'")
        
        print("\n✅ Text processor tests passed!\n")
        return True
        
    except Exception as e:
        print(f"❌ Text processor error: {str(e)}")
        return False


def test_scorer():
    """Test scoring logic"""
    print("🧪 Testing scorer...")
    
    try:
        from src.models.schemas import CriteriaScore
        from src.pipeline.scorer import Scorer
        
        score = CriteriaScore(
            technique=75,
            defense=80,
            attitude=85,
            physique=78,
            decision_tactique=72,
            autre=70,
        )
        
        final_score = Scorer.calculate_final_score(score)
        print(f"  ✅ Final score calculated: {final_score}/100")
        
        category = Scorer.get_rating_category(final_score)
        print(f"  ✅ Rating category: {category}")
        
        color = Scorer.get_score_color(final_score)
        print(f"  ✅ Score color: {color}")
        
        print("\n✅ Scorer tests passed!\n")
        return True
        
    except Exception as e:
        print(f"❌ Scorer error: {str(e)}")
        return False


def check_env():
    """Check environment setup"""
    print("🔧 Checking environment setup...")
    
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and groq_key != "your_groq_api_key_here":
        print("  ✅ GROQ_API_KEY configured")
    else:
        print("  ⚠️  GROQ_API_KEY not set (required for LLM)")
    
    ffmpeg_path = os.getenv("FFMPEG_PATH")
    if ffmpeg_path:
        print(f"  ✅ FFMPEG_PATH set: {ffmpeg_path}")
    else:
        print("  ⚠️  FFMPEG_PATH not set (required for audio)")
    
    print()


def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 Volleyball Commentary Analyzer - Quick Test")
    print("=" * 60)
    print()
    
    check_env()
    
    all_passed = True
    
    if not test_imports():
        all_passed = False
    
    if not test_basic_validation():
        all_passed = False
    
    if not test_text_processor():
        all_passed = False
    
    if not test_scorer():
        all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("✅ All tests passed! Ready to run the application.")
        print()
        print("Next steps:")
        print("  1. Configure .env with your GROQ_API_KEY")
        print("  2. Run: streamlit run main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    print("=" * 60)


if __name__ == "__main__":
    main()
