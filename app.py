import streamlit as st
from src.Pipelines.pipeline import (
    build_search_agent, build_reader_agent, writer_chain, critic_chain, extract_text
)

# ── Page config ──
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="\U0001F9E0",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,400;0,500;0,700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #edf3ff;
}

.stApp {
    background: #07111f;
    background-image:
        radial-gradient(circle at top left, rgba(0,191,255,0.14), transparent 32%),
        radial-gradient(circle at bottom right, rgba(124,58,237,0.12), transparent 30%),
        linear-gradient(180deg, #07111f 0%, #0a1729 100%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

.eyebrow {
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.25em;
    font-size: 0.75rem;
    color: #5fd4ff;
    text-align: center;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 4.5rem;
    text-align: center;
    background: linear-gradient(90deg, #4fc3f7, #8b7cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.3rem 0 1rem;
}

.hero-sub {
    text-align: center;
    color: #9fb0c9;
    font-size: 1.05rem;
    max-width: 640px;
    margin: 0 auto 2.5rem;
    line-height: 1.6;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(95,212,255,0.4), transparent);
    margin: 0.5rem 0 2.5rem;
}

.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.6rem;
}

.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    color: #5fd4ff;
    margin-bottom: 0.5rem;
}

.section-heading {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: #edf3ff;
    margin-bottom: 1rem;
}

.stage-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.9rem;
}

.stage-num {
    font-family: 'DM Mono', monospace;
    color: #5fd4ff;
    font-size: 0.85rem;
}

.stage-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    margin: 0.2rem 0 0.15rem;
}

.stage-desc {
    color: #8ba0bd;
    font-size: 0.85rem;
}

.stage-status {
    float: right;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    padding: 3px 10px;
    border-radius: 20px;
}

.status-waiting { background: rgba(255,255,255,0.06); color: #7c8ba3; }
.status-running { background: rgba(95,212,255,0.15); color: #5fd4ff; }
.status-done { background: rgba(99,217,163,0.15); color: #63d9a3; }

.result-panel {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 1.2rem;
}

.result-panel-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    color: #5fd4ff;
    margin-bottom: 0.6rem;
}

.result-content {
    color: #c3d2e8;
    font-size: 0.9rem;
    line-height: 1.6;
    white-space: pre-wrap;
}

.report-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 18px;
    padding: 2.2rem 2.5rem;
    line-height: 1.75;
}

.critic-box {
    background: linear-gradient(135deg, rgba(139,124,246,0.08), rgba(0,191,255,0.05));
    border: 1px solid rgba(139,124,246,0.25);
    border-radius: 18px;
    padding: 2.2rem 2.5rem;
    line-height: 1.75;
}

.stButton>button {
    background: linear-gradient(90deg, #4fc3f7, #8b7cf6);
    color: #07111f;
    border: none;
    border-radius: 10px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    transition: transform 0.15s ease;
}
.stButton>button:hover { transform: translateY(-2px); }

.chip-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──
st.markdown('<div class="eyebrow">MULTI-AGENT AI SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">ResearcherAgent</div>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Four specialized AI agents collaborate — searching, scraping, writing, '
    'and critiquing — to deliver a polished research report on any topic.</p>',
    unsafe_allow_html=True,
)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Layout: input left, pipeline right ──
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

SUGGESTIONS = [
    "Future of LLMs in tech industry",
    "All latest AI agents in 2026",
    "Roadmap for AGI development in next 5 years",
]

if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    st.markdown('<div class="section-label">RESEARCH TOPIC</div>', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Roadmap for AGI development in next 5 years",
        key="topic_input",
        label_visibility="collapsed",
    )

    run_btn = st.button("\u26A1 Run Research Pipeline", use_container_width=True)

    st.markdown('<div class="section-label" style="margin-top:1.2rem;">TRY \u2192</div>', unsafe_allow_html=True)
    chip_cols = st.columns(len(SUGGESTIONS))
    for i, s in enumerate(SUGGESTIONS):
        if chip_cols[i].button(s, key=f"chip_{i}", use_container_width=True):
            st.session_state.topic_input = s
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    stage_defs = [
        ("01", "Search Agent", "Gathers recent web information"),
        ("02", "Reader Agent", "Scrapes & extracts deep content"),
        ("03", "Writer Chain", "Drafts the full research report"),
        ("04", "Critic Chain", "Reviews & scores the report"),
    ]
    stage_placeholders = []
    for num, title, desc in stage_defs:
        ph = st.empty()
        stage_placeholders.append(ph)
        ph.markdown(f'''
            <div class="stage-box">
                <span class="stage-status status-waiting">WAITING</span>
                <div class="stage-num">{num}</div>
                <div class="stage-title">{title}</div>
                <div class="stage-desc">{desc}</div>
            </div>
        ''', unsafe_allow_html=True)


def set_stage(idx, status, title, desc, num):
    cls = {"running": "status-running", "done": "status-done", "waiting": "status-waiting"}[status]
    label = {"running": "RUNNING", "done": "DONE", "waiting": "WAITING"}[status]
    stage_placeholders[idx].markdown(f'''
        <div class="stage-box">
            <span class="stage-status {cls}">{label}</span>
            <div class="stage-num">{num}</div>
            <div class="stage-title">{title}</div>
            <div class="stage-desc">{desc}</div>
        </div>
    ''', unsafe_allow_html=True)


# ── Run pipeline ──
if run_btn and topic:
    r = {}

    set_stage(0, "running", "Search Agent", "Gathers recent web information", "01")
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    r["search"] = extract_text(search_result['messages'][-1].content)
    set_stage(0, "done", "Search Agent", "Gathers recent web information", "01")

    set_stage(1, "running", "Reader Agent", "Scrapes & extracts deep content", "02")
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{r['search'][:800]}"
        )]
    })
    r["reader"] = extract_text(reader_result['messages'][-1].content)
    set_stage(1, "done", "Reader Agent", "Scrapes & extracts deep content", "02")

    set_stage(2, "running", "Writer Chain", "Drafts the full research report", "03")
    research_combined = f"SEARCH RESULTS : \n {r['search']} \n\nDETAILED SCRAPED CONTENT : \n {r['reader']}"
    r["writer"] = writer_chain.invoke({"topic": topic, "research": research_combined})
    set_stage(2, "done", "Writer Chain", "Drafts the full research report", "03")

    set_stage(3, "running", "Critic Chain", "Reviews & scores the report", "04")
    r["critic"] = critic_chain.invoke({"report": r["writer"]})
    set_stage(3, "done", "Critic Chain", "Reviews & scores the report", "04")

    st.session_state.results = r

r = st.session_state.get("results")

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("\U0001F50D Search Results (raw)", expanded=False):
            st.markdown(f'''
                <div class="result-panel">
                    <div class="result-panel-title">SEARCH AGENT OUTPUT</div>
                    <div class="result-content">{r["search"]}</div>
                </div>
            ''', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("\U0001F4C4 Scraped Content (raw)", expanded=False):
            st.markdown(f'''
                <div class="result-panel">
                    <div class="result-panel-title">READER AGENT OUTPUT</div>
                    <div class="result-content">{r["reader"]}</div>
                </div>
            ''', unsafe_allow_html=True)

    if "writer" in r:
        st.markdown('<div class="section-label" style="margin-top:1.5rem;">FINAL RESEARCH REPORT</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="report-box">{r["writer"]}</div>', unsafe_allow_html=True)

    if "critic" in r:
        st.markdown('<div class="section-label" style="margin-top:1.5rem;">CRITIC FEEDBACK</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="critic-box">{r["critic"]}</div>', unsafe_allow_html=True)

st.markdown(
    '<p style="text-align:center; color:#4a5b73; font-family:\'DM Mono\',monospace; '
    'font-size:0.75rem; margin-top:3rem;">ResearchAgent &middot; Powered by LangChain multi-agent pipeline &middot; Built with Streamlit</p>',
    unsafe_allow_html=True,
)