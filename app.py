import streamlit as st
import time
from pipeline import run_research_pipeline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,400;0,500;1,400&display=swap');

  /* ── Global reset ── */
  html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0b0c10;
    color: #e8e6e1;
  }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 2.5rem 3rem 4rem 3rem; max-width: 1100px; }

  /* ── Hero header ── */
  .hero {
    border-left: 4px solid #00d4aa;
    padding: 1.2rem 1.6rem;
    margin-bottom: 2.5rem;
    background: linear-gradient(135deg, rgba(0,212,170,0.06) 0%, transparent 60%);
  }
  .hero h1 {
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin: 0 0 0.3rem 0;
    color: #ffffff;
  }
  .hero p {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #00d4aa;
    margin: 0;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  /* ── Input area ── */
  .stTextInput > div > div > input {
    background: #13151a !important;
    border: 1.5px solid #2a2d35 !important;
    border-radius: 8px !important;
    color: #e8e6e1 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
  }
  .stTextInput > div > div > input:focus {
    border-color: #00d4aa !important;
    box-shadow: 0 0 0 3px rgba(0,212,170,0.12) !important;
  }
  .stTextInput > div > div > input::placeholder { color: #555a66 !important; }

  /* ── Button ── */
  .stButton > button {
    background: #00d4aa !important;
    color: #0b0c10 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 2rem !important;
    transition: background 0.2s, transform 0.1s !important;
    text-transform: uppercase !important;
  }
  .stButton > button:hover {
    background: #00b894 !important;
    transform: translateY(-1px) !important;
  }
  .stButton > button:active { transform: translateY(0) !important; }

  /* ── Pipeline steps ── */
  .pipeline-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0;
    margin: 2rem 0;
    border: 1px solid #1e2128;
    border-radius: 10px;
    overflow: hidden;
  }
  .pipeline-step {
    padding: 1.1rem 1rem;
    text-align: center;
    background: #13151a;
    border-right: 1px solid #1e2128;
    transition: background 0.3s;
    position: relative;
  }
  .pipeline-step:last-child { border-right: none; }
  .pipeline-step .step-icon { font-size: 1.5rem; margin-bottom: 0.4rem; display: block; }
  .pipeline-step .step-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #555a66;
  }
  .pipeline-step .step-name {
    font-size: 0.82rem;
    font-weight: 600;
    color: #9da3b0;
    margin-top: 0.2rem;
  }
  .pipeline-step.active {
    background: rgba(0,212,170,0.08);
  }
  .pipeline-step.active .step-label { color: #00d4aa; }
  .pipeline-step.active .step-name  { color: #e8e6e1; }
  .pipeline-step.done {
    background: rgba(0,212,170,0.04);
  }
  .pipeline-step.done .step-label { color: #00a884; }
  .pipeline-step.done .step-name  { color: #a0a8b5; }

  /* ── Result cards ── */
  .result-card {
    background: #13151a;
    border: 1px solid #1e2128;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
  }
  .result-card-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 1rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid #1e2128;
  }
  .result-card-header .badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.66rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    background: rgba(0,212,170,0.12);
    color: #00d4aa;
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
  }
  .result-card-header h3 {
    font-size: 0.95rem;
    font-weight: 700;
    margin: 0;
    color: #e8e6e1;
  }
  .result-card-content {
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    line-height: 1.75;
    color: #9da3b0;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 320px;
    overflow-y: auto;
  }
  .result-card-content::-webkit-scrollbar { width: 4px; }
  .result-card-content::-webkit-scrollbar-track { background: transparent; }
  .result-card-content::-webkit-scrollbar-thumb { background: #2a2d35; border-radius: 2px; }

  /* ── Final report special card ── */
  .report-card {
    background: linear-gradient(135deg, #13151a 0%, #161a22 100%);
    border: 1px solid #00d4aa33;
    border-radius: 10px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.2rem;
  }
  .report-card-content {
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
    line-height: 1.85;
    color: #c8c4bc;
    white-space: pre-wrap;
    word-break: break-word;
  }

  /* ── Divider ── */
  .section-divider {
    height: 1px;
    background: linear-gradient(90deg, #00d4aa33, transparent);
    margin: 2rem 0;
  }

  /* ── Status pill ── */
  .status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    margin-bottom: 1.5rem;
  }
  .status-pill.running  { background: rgba(255,180,0,0.12);  color: #ffb400; }
  .status-pill.success  { background: rgba(0,212,170,0.12);  color: #00d4aa; }
  .status-pill.error    { background: rgba(255,80,80,0.12);   color: #ff5050; }

  /* Spinner tweak */
  .stSpinner > div { border-top-color: #00d4aa !important; }
</style>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <p>🔬 &nbsp; Multi-Agent Research System</p>
  <h1>Research Intelligence<br>Pipeline</h1>
</div>
""", unsafe_allow_html=True)


# ── Pipeline visualiser (static legend) ───────────────────────────────────────
STEPS = [
    ("🔍", "Step 01", "Search Agent"),
    ("📄", "Step 02", "Reader Agent"),
    ("✍️",  "Step 03", "Writer Chain"),
    ("🧠", "Step 04", "Critic Chain"),
]

def render_pipeline(active: int = -1, done_up_to: int = -1):
    """active = 0-indexed step currently running; done_up_to = steps finished."""
    cols_html = ""
    for i, (icon, label, name) in enumerate(STEPS):
        cls = "pipeline-step"
        if i == active:
            cls += " active"
        elif i <= done_up_to:
            cls += " done"
        step_icon = "✅" if i <= done_up_to and i != active else icon
        cols_html += f"""
        <div class="{cls}">
          <span class="step-icon">{step_icon}</span>
          <div class="step-label">{label}</div>
          <div class="step-name">{name}</div>
        </div>"""
    st.markdown(f'<div class="pipeline-grid">{cols_html}</div>', unsafe_allow_html=True)


# ── Input ─────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1], gap="small")
with col_input:
    topic = st.text_input(
        label="Research Topic",
        placeholder="e.g. Latest breakthroughs in quantum computing 2025",
        label_visibility="collapsed",
    )
with col_btn:
    run_btn = st.button("Run →", use_container_width=True)


# ── Session state ──────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "error"  not in st.session_state:
    st.session_state.error  = None

# ── Default pipeline view (idle) ─────────────────────────────────────────────
if not run_btn and st.session_state.result is None and st.session_state.error is None:
    render_pipeline()


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.result = None
        st.session_state.error  = None

        status_placeholder    = st.empty()
        pipeline_placeholder  = st.empty()
        spinner_placeholder   = st.empty()

        # Helper to update the pipeline display
        def update_step(active_idx, done_idx):
            with pipeline_placeholder.container():
                render_pipeline(active=active_idx, done_up_to=done_idx)

        try:
            # ── Step 1: Search ────────────────────────────────────────────
            status_placeholder.markdown(
                '<div class="status-pill running">⚡ Running — Search Agent</div>',
                unsafe_allow_html=True,
            )
            update_step(0, -1)
            with spinner_placeholder:
                with st.spinner("Search Agent is gathering information..."):
                    from agents import build_search_agent
                    search_agent  = build_search_agent()
                    search_result = search_agent.invoke({
                        "messages": [("user", f"Find recent and detailed information about: {topic}")]
                    })
                    search_results = search_result["messages"][-1].content

            # ── Step 2: Reader ────────────────────────────────────────────
            status_placeholder.markdown(
                '<div class="status-pill running">⚡ Running — Reader Agent</div>',
                unsafe_allow_html=True,
            )
            update_step(1, 0)
            with spinner_placeholder:
                with st.spinner("Reader Agent is scraping top resources..."):
                    from agents import build_reader_agent
                    reader_agent  = build_reader_agent()
                    reader_result = reader_agent.invoke({
                        "messages": [("user",
                            f"Based on the following search result about '{topic}', "
                            f"pick the most relevant URL and scrape it for deeper content.\n\n"
                            f"Search Results:\n{search_results[:800]}"
                        )]
                    })
                    scraped_content = reader_result["messages"][-1].content

            # ── Step 3: Writer ────────────────────────────────────────────
            status_placeholder.markdown(
                '<div class="status-pill running">⚡ Running — Writer Chain</div>',
                unsafe_allow_html=True,
            )
            update_step(2, 1)
            with spinner_placeholder:
                with st.spinner("Writer Chain is drafting the report..."):
                    from agents import writer_chain
                    research_combined = (
                        f"Search Results:\n{search_results}\n\n"
                        f"Scraped Content:\n{scraped_content}"
                    )
                    report = writer_chain.invoke({"topic": topic, "research": research_combined})

            # ── Step 4: Critic ────────────────────────────────────────────
            status_placeholder.markdown(
                '<div class="status-pill running">⚡ Running — Critic Chain</div>',
                unsafe_allow_html=True,
            )
            update_step(3, 2)
            with spinner_placeholder:
                with st.spinner("Critic Chain is evaluating the report..."):
                    from agents import critic_chain
                    feedback = critic_chain.invoke({"report": report})

            # ── Done ──────────────────────────────────────────────────────
            spinner_placeholder.empty()
            status_placeholder.markdown(
                '<div class="status-pill success">✅ Pipeline Complete</div>',
                unsafe_allow_html=True,
            )
            update_step(-1, 3)

            st.session_state.result = {
                "search_results": search_results,
                "scraped_content": scraped_content,
                "report": report,
                "feedback": feedback,
            }

        except Exception as e:
            spinner_placeholder.empty()
            status_placeholder.markdown(
                '<div class="status-pill error">✗ Pipeline Error</div>',
                unsafe_allow_html=True,
            )
            st.session_state.error = str(e)


# ── Error display ──────────────────────────────────────────────────────────────
if st.session_state.error:
    st.error(f"**Error:** {st.session_state.error}")


# ── Results ────────────────────────────────────────────────────────────────────
if st.session_state.result:
    res = st.session_state.result

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### Research Output")

    # ── Intermediate results in tabs ──────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["🔍 Search Results", "📄 Scraped Content", "🧠 Critic Feedback"])

    with tab1:
        st.markdown(f"""
        <div class="result-card">
          <div class="result-card-header">
            <span class="badge">Step 01</span>
            <h3>Search Agent Output</h3>
          </div>
          <div class="result-card-content">{res["search_results"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown(f"""
        <div class="result-card">
          <div class="result-card-header">
            <span class="badge">Step 02</span>
            <h3>Reader Agent — Scraped Content</h3>
          </div>
          <div class="result-card-content">{res["scraped_content"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown(f"""
        <div class="result-card">
          <div class="result-card-header">
            <span class="badge">Step 04</span>
            <h3>Critic Chain Feedback</h3>
          </div>
          <div class="result-card-content">{res["feedback"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Final Report ──────────────────────────────────────────────────────
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📋 Final Report")
    st.markdown(f"""
    <div class="report-card">
      <div class="result-card-header" style="border-bottom:1px solid #00d4aa22; margin-bottom:1.2rem; padding-bottom:0.8rem;">
        <span class="badge">Step 03</span>
        <h3>Writer Chain — Research Report</h3>
      </div>
      <div class="report-card-content">{res["report"]}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Download button ───────────────────────────────────────────────────
    st.download_button(
        label="⬇  Download Report (.txt)",
        data=res["report"],
        file_name=f"research_report_{topic[:40].replace(' ', '_')}.txt",
        mime="text/plain",
    )