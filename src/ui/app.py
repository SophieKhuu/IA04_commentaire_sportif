"""
Main Streamlit application for Volleyball Commentary Analyzer
"""

import time
import logging
import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Optional

from src.config import SCORING_CRITERIA, GROQ_API_KEY
from src.pipeline.llm_client import GroqLLMClient
from src.pipeline.extractor import AnalysisExtractor, ExtractionError
from src.pipeline.scorer import Scorer
from src.pipeline.transcriber import WhisperTranscriber
from src.pipeline.text_processor import TextProcessor
from src.models.schemas import AnalysisResult, ExportResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Volleyball Commentary Analyzer",
    page_icon="🏐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .score-excellent { color: #006400; font-weight: bold; }
    .score-good { color: #FFD700; font-weight: bold; }
    .score-poor { color: #DC143C; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_llm_client():
    """Initialize LLM client (cached)"""
    if not GROQ_API_KEY:
        st.error("⚠️ GROQ_API_KEY not configured. Please set it in .env file")
        st.stop()
    return GroqLLMClient()


@st.cache_resource
def get_transcriber():
    """Initialize Whisper transcriber (cached)"""
    return WhisperTranscriber()


def render_header():
    """Render application header"""
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.title("🏐 Volleyball Commentary Analyzer")
        st.markdown(
            "Analyze sports commentary with AI to generate player performance ratings"
        )
    with col2:
        st.markdown("v0.1.0")


def render_sidebar():
    """Render sidebar configuration"""
    with st.sidebar:
        st.header("⚙️ Configuration")

        st.subheader("Scoring Weights")
        weights = {}
        for criterion_key, criterion_info in SCORING_CRITERIA.items():
            weights[criterion_key] = st.slider(
                criterion_info["name"],
                0.0,
                1.0,
                criterion_info["weight"],
                0.05,
                help=criterion_info["description"],
            )

        # Normalize weights
        total = sum(weights.values())
        if total > 0:
            weights = {k: v / total for k, v in weights.items()}

        st.divider()
        st.subheader("About")
        st.markdown(
            """
        This application analyzes volleyball commentary using advanced LLM models
        to extract player performance metrics and generate ratings.

        **Key Features:**
        - Text & audio input support
        - 6-criteria performance scoring
        - JSON/CSV export
        - Real-time analysis
        """
        )

        return weights


def render_analysis_tab(weights):
    """Render main analysis tab"""
    st.header("📝 Analyze Commentary")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Text Input")
        commentary_text = st.text_area(
            "Enter or paste commentary",
            placeholder="Describe the player performance...",
            height=200,
            key="text_input",
        )

    with col2:
        st.subheader("Audio Input")
        audio_file = st.file_uploader(
            "Upload audio file (MP3, WAV, M4A, OGG)",
            type=["mp3", "wav", "m4a", "ogg"],
        )
        transcribed_text = None

        if audio_file is not None:
            with st.spinner("🎤 Transcribing audio..."):
                try:
                    # Save uploaded file temporarily
                    import tempfile
                    import os

                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=audio_file.name
                    ) as tmp_file:
                        tmp_file.write(audio_file.getbuffer())
                        tmp_path = tmp_file.name

                    transcriber = get_transcriber()
                    transcribed_text = transcriber.transcribe(tmp_path)

                    # Clean up
                    os.unlink(tmp_path)

                    st.success("✅ Transcription completed")
                    st.text_area(
                        "Transcribed text",
                        value=transcribed_text,
                        height=100,
                        disabled=True,
                    )

                except Exception as e:
                    st.error(f"❌ Transcription failed: {str(e)}")

    # Decide which text to use
    text_to_analyze = transcribed_text if transcribed_text else commentary_text

    # Analysis button
    if st.button("🚀 Analyze", use_container_width=True, type="primary"):
        if not text_to_analyze or not text_to_analyze.strip():
            st.error("❌ Please enter or transcribe a commentary")
            return

        # Validate
        if not TextProcessor.validate_commentary(text_to_analyze):
            st.error(
                f"❌ Commentary validation failed. "
                f"Please provide 10-5000 words."
            )
            return

        # Analyze
        with st.spinner("🔄 Analyzing with LLM..."):
            try:
                start_time = time.time()

                # Get LLM client and analyze
                llm_client = get_llm_client()
                llm_response = llm_client.extract_json(text_to_analyze)

                processing_time = time.time() - start_time

                # Extract ratings
                player_ratings = AnalysisExtractor.extract_player_ratings(
                    llm_response,
                    llm_response.get("summary", ""),
                    source_type="audio" if audio_file else "text",
                )

                # Build result
                analysis_result = AnalysisExtractor.build_analysis_result(
                    commentary=text_to_analyze,
                    llm_response=llm_response,
                    player_ratings=player_ratings,
                    processing_time=processing_time,
                    metadata={"weights": weights},
                )

                # Store in session state
                st.session_state.last_analysis = analysis_result

                # Display results
                render_results(analysis_result, weights)

            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                logger.error(f"Analysis error: {str(e)}", exc_info=True)


def render_results(analysis_result: AnalysisResult, weights: dict):
    """Render analysis results"""
    st.success("✅ Analysis completed!")

    # Summary
    st.subheader("📊 Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Players Found", len(analysis_result.players))
    with col2:
        avg_score = (
            sum(p.final_score for p in analysis_result.players)
            / len(analysis_result.players)
            if analysis_result.players
            else 0
        )
        st.metric("Average Score", f"{avg_score:.1f}")
    with col3:
        st.metric(
            "Processing Time", f"{analysis_result.processing_time_seconds:.2f}s"
        )

    st.markdown(f"**Summary:** {analysis_result.summary}")

    # Player ratings table
    if analysis_result.players:
        st.subheader("🏐 Player Ratings")

        # Prepare DataFrame
        data = []
        for player in analysis_result.players:
            data.append(
                {
                    "Name": player.name,
                    "Number": player.number or "-",
                    "Technique": player.scores.technique,
                    "Defense": player.scores.defense,
                    "Attitude": player.scores.attitude,
                    "Physique": player.scores.physique,
                    "Decision": player.scores.decision_tactique,
                    "Other": player.scores.autre,
                    "Final Score": f"{player.final_score:.1f}",
                    "Category": Scorer.get_rating_category(player.final_score),
                }
            )

        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

        # Export options
        st.subheader("📥 Export")
        col1, col2 = st.columns(2)

        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"volleyball_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
            )

        with col2:
            import json

            json_data = analysis_result.model_dump_json(indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"volleyball_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
            )

        # Detailed view
        st.subheader("📋 Detailed Ratings")
        for player in analysis_result.players:
            with st.expander(f"{player.name} (#{player.number})" if player.number else player.name):
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Final Score", f"{player.final_score}/100")
                    st.metric("Category", Scorer.get_rating_category(player.final_score))

                with col2:
                    # Criteria breakdown
                    criteria_data = {
                        "Criterion": list(SCORING_CRITERIA.keys()),
                        "Score": [
                            player.scores.technique,
                            player.scores.defense,
                            player.scores.attitude,
                            player.scores.physique,
                            player.scores.decision_tactique,
                            player.scores.autre,
                        ],
                    }
                    criteria_df = pd.DataFrame(criteria_data)
                    st.bar_chart(criteria_df.set_index("Criterion"))

                st.markdown(f"**Notes:** {player.notes}")
                if player.facts:
                    st.markdown("**Key Facts:**")
                    for fact in player.facts:
                        st.markdown(f"- {fact}")


def render_history_tab():
    """Render history and export tab"""
    st.header("📜 Analysis History")

    if "analysis_history" not in st.session_state:
        st.session_state.analysis_history = []

    if "last_analysis" in st.session_state:
        analysis = st.session_state.last_analysis
        st.session_state.analysis_history.append(analysis)

    if not st.session_state.analysis_history:
        st.info("No analyses yet. Start by analyzing a commentary.")
        return

    st.success(f"Total analyses: {len(st.session_state.analysis_history)}")

    # Display all analyses
    for idx, analysis in enumerate(st.session_state.analysis_history[-10:]):  # Show last 10
        with st.expander(
            f"Analysis {idx + 1} - {analysis.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Players:** {len(analysis.players)}")
                st.markdown(f"**Type:** {analysis.source_type}")
            with col2:
                st.markdown(f"**Model:** {analysis.model_used}")
                st.markdown(f"**Time:** {analysis.processing_time_seconds:.2f}s")

            st.markdown("**Summary:**")
            st.markdown(analysis.summary)


def main():
    """Main application entry point"""
    render_header()

    weights = render_sidebar()

    # Main tabs
    tab1, tab2 = st.tabs(["📝 Analysis", "📜 History"])

    with tab1:
        render_analysis_tab(weights)

    with tab2:
        render_history_tab()
