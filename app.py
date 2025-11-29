# app.py — Streamlit frontend for MARS (FINAL, Option B: Large centered logo)
import os
import sys
import time
from typing import Dict, List
<<<<<<< HEAD

import streamlit as st
=======
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
>>>>>>> ec1bd1a (Upload full local project)

# ensure repo import works (src/ must be in repo root)
sys.path.append(os.path.join(os.path.dirname(__file__), ""))

# Try to import the orchestrator pipeline
try:
    from src.orchestrator import answer_query
except Exception:
    answer_query = None
    import traceback
    _import_error = traceback.format_exc()
else:
    _import_error = None

st.set_page_config(
    page_title="MARS — Multi-Agent Research Assistant",
    page_icon="🚀",
    layout="wide",
)

# ---- Logo (Large, centered) ----
repo_image_path = "docs/logo.png"  # preferred for deployed app (Streamlit Cloud)

# show large centered logo
if os.path.exists(repo_image_path):
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image(repo_image_path, width=420, use_column_width=False)
else:
    st.markdown("<h3 style='text-align:center;'>MARS</h3>", unsafe_allow_html=True)

# ---- Title & subtitle ----
st.markdown("<br/>", unsafe_allow_html=True)
st.title("🚀 MARS — Multi-Agent Research Assistant")
st.markdown(
    "Ask a question and MARS will search the web live, store evidence in memory, and return a concise, citation-based summary with fact-check signals."
)

st.markdown("---")

# ---- Sidebar settings ----
with st.sidebar:
    st.header("Settings")
    st.info("Set API keys in Streamlit Cloud (see Deploy steps).")
    pages_to_search = st.slider("Max pages to search (per query)", min_value=1, max_value=10, value=3)
    top_k = st.slider("Number of retrieved chunks (top_k)", min_value=1, max_value=10, value=5)
    user_id = st.text_input("User ID (optional)", value="", help="Leave empty for global memory.")
    show_prompt = st.checkbox("Show RAG prompt (debug)", value=False)
    st.markdown("")

st.write("### Ask MARS a question (live web)")
query = st.text_input("Enter your query here", value="", max_chars=300)

col1, col2 = st.columns([1, 3])
with col1:
    run_btn = st.button("🚀 Run MARS")
with col2:
    st.write("Tip: try `Impact of AI on healthcare in 2025`")

# placeholders
answer_placeholder = st.container()
sources_placeholder = st.container()
factcheck_placeholder = st.container()
metrics_placeholder = st.container()

def run_pipeline_and_display(query_text: str, pages: int, top_k_val: int, user: str):
    ts0 = time.time()
    try:
        if answer_query is None:
            st.error("Orchestrator import failed. Make sure src/orchestrator.py exists and is valid.")
            if _import_error:
                st.code(_import_error, language="py")
            return

        with st.spinner("Running research, ingesting, retrieving, and generating summary..."):
            out: Dict = answer_query(query_text, top_k=top_k_val)

        # Summary
        with answer_placeholder:
            st.markdown("## 📝 Summary")
            st.write(out.get("final_output", "No summary produced."))

        # Fact-check
        fc = out.get("fact_check", {})
        supported = len(fc.get("supported", [])) if fc else 0
        not_supported = len(fc.get("not_supported", [])) if fc else 0
        total_claims = fc.get("total_claims", 0) if fc else 0

        with factcheck_placeholder:
            st.markdown("## ✅ Fact-Check")
            if total_claims == 0:
                st.info("No explicit claims detected in the summary.")
            else:
                c1, c2, c3 = st.columns([1,1,2])
                c1.metric("Supported", f"{supported}/{total_claims}")
                c2.metric("Unsupported", f"{not_supported}/{total_claims}")
                with c3:
                    if not_supported > 0:
                        st.warning("Some statements could not be verified from retrieved sources.")
                    else:
                        st.success("All claims supported by retrieved context.")

        # Sources
        with sources_placeholder:
            st.markdown("## 🔗 Sources (top results)")
            sources: List[str] = out.get("sources", []) or []
            if sources:
                for s in sources:
                    st.markdown(f"- [{s}]({s})")
            else:
                st.info("No explicit source list available. Try increasing pages or check logs.")

        # Metrics
        t_elapsed = time.time() - ts0
        with metrics_placeholder:
            st.markdown(f"**Elapsed:** {t_elapsed:.1f}s | pages searched: {pages} | top_k: {top_k_val}")

        # Show prompt optionally
        if show_prompt:
            with st.expander("RAG prompt (if available)", expanded=False):
                prompt_text = out.get("prompt", None)
                if prompt_text:
                    st.code(prompt_text)
                else:
                    st.info("No prompt captured by the orchestrator.")

    except Exception as e:
        st.exception(e)

if run_btn and query.strip():
    run_pipeline_and_display(query.strip(), pages_to_search, top_k, user_id)

st.markdown("---")
st.caption("MARS — Multi-Agent Research Assistant • Live web, RAG, and fact-check. Built for the Google AI Intensive Capstone.")

# ===== Gradient Signature Footer (Option 2) =====
st.markdown(
    """
    <div style='
        margin-top: 18px;
        text-align: center;
        font-size: 18px;
        font-weight: 700;
        background: linear-gradient(90deg,#ff7b00,#e600ff);
        -webkit-background-clip: text;
        color: transparent;
    '>
        Crafted with ❤️ by Sriteja • Arnav • Snehal
    </div>
    <div style='text-align:center; font-size:14px; color:gray; margin-top:6px;'>
        © 2025 MARS — Multi-Agent Research Assistant
    </div>
    """,
    unsafe_allow_html=True
)
