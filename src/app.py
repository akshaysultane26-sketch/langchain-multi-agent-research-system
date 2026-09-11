import streamlit as st
from src.Pipelines.pipeline import (
    build_search_agent, build_reader_agent, writer_chain, critic_chain, extract_text
)

st.set_page_config(page_title="AI Research System", page_icon="🔎", layout="centered")

st.markdown("""
<style>
.main-title { font-size: 2.2rem; font-weight: 700; text-align: center; margin-bottom: 0.2rem; }
.subtitle { text-align: center; color: #888; margin-bottom: 2rem; }
.stage-card { background: #1e1e1e; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1rem; border-left: 4px solid #4CAF50; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔎 AI Research System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Multi-agent research, writing & critique — powered by Gemini</div>', unsafe_allow_html=True)

topic = st.text_input("Enter a research topic", placeholder="e.g. latest developments in AI agents")
run = st.button("Run Research Pipeline", type="primary", use_container_width=True)

if run and topic:
    state = {}

    with st.status("Step 1 · Searching the web...", expanded=True) as status:
        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        state["search_results"] = extract_text(search_result['messages'][-1].content)
        st.write(state["search_results"][:500] + "...")
        status.update(label="Step 1 · Search complete", state="complete")

    with st.status("Step 2 · Reading top sources...", expanded=True) as status:
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
        state['scraped_content'] = extract_text(reader_result['messages'][-1].content)
        st.write(state['scraped_content'][:500] + "...")
        status.update(label="Step 2 · Reading complete", state="complete")

    with st.status("Step 3 · Writing the report...", expanded=False) as status:
        research_combined = (
            f"SEARCH RESULTS : \n {state['search_results']} \n\n"
            f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
        status.update(label="Step 3 · Report drafted", state="complete")

    with st.status("Step 4 · Critic reviewing...", expanded=False) as status:
        state["feedback"] = critic_chain.invoke({"report": state['report']})
        status.update(label="Step 4 · Review complete", state="complete")

    st.divider()
    st.markdown("## 📄 Final Report")
    st.markdown(f'<div class="stage-card">{state["report"]}</div>', unsafe_allow_html=True)

    st.markdown("## 🧐 Critic Feedback")
    st.markdown(f'<div class="stage-card">{state["feedback"]}</div>', unsafe_allow_html=True)

elif run and not topic:
    st.warning("Please enter a topic first.")
    