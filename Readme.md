# LangChain Multi-Agent Research System

A powerful multi-agent research system built with LangChain that autonomously researches topics, gathers information, writes comprehensive reports, and evaluates their quality using AI-powered agents.

`Research Automation` · `Multi-Agent Orchestration` · `Intelligent Report Generation`

---

## 🌟 Features

- **Multi-Agent Architecture**: Specialized agents for searching, reading, writing, and critiquing
- **Automated Web Research**: Intelligent web search using DuckDuckGo
- **Smart Content Extraction**: Advanced web scraping with multiple fallback strategies (trafilatura → readability → BeautifulSoup)
- **AI-Powered Report Generation**: Automatically generates structured research reports
- **Quality Evaluation**: Built-in critic agent for report validation and scoring
- **Interactive UI**: Streamlit-based interface for easy interaction
- **Pipeline Orchestration**: Seamless coordination of multiple agents

---

## 🏗️ Architecture
Streamlit UI (app.py)
Multi-Agent Research Assistant Interface
│
▼
Research Pipeline (pipeline.py)
Orchestrates multi-agent workflow
│
▼
┌─────────────┬──────────────┬─────────────┐
│ Search Agent │ Reader Agent │ Writer Chain │
└─────────────┴──────────────┴─────────────┘
│
▼
Tools Layer
• web_search
• scrape_url
│
▼
Critic Chain 

### Agent Responsibilities

- **Search Agent**: Discovers relevant information across the web using DuckDuckGo
- **Reader Agent**: Extracts clean, readable content from URLs
- **Writer Chain**: Composes structured, professional research reports
- **Critic Chain**: Evaluates reports and provides improvement suggestions

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| LangChain | Multi-agent orchestration and chain management |
| Google Gemini (gemini-flash-lite-latest) | Language model for agents and chains |
| Streamlit | Interactive web UI |
| DuckDuckGo Search | Web search and information retrieval |
| BeautifulSoup4 | HTML parsing and content extraction |
| Trafilatura | Web content extraction |
| Readability-lxml | Article content extraction |
| python-dotenv | Environment configuration management |

---

## 📋 Prerequisites

- Python 3.11 or higher
- Google API Key (for Gemini)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/akshaysultane26-sketch/langchain-multi-agent-research-system.git
cd langchain-multi-agent-research-system
```

### 2. Create Environment

```bash
python -m venv myenv
myenv\Scripts\activate   # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

GOOGLE_API_KEY=your_google_api_key_here

Get your key from:
- [Google AI Studio](https://aistudio.google.com/apikey)

---

## 💡 Usage

### Run with Streamlit UI (Recommended)

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

### Run as a Script

```bash
python -m src.Pipelines.pipeline
```

Edit the `topic` variable inside `pipeline.py`'s `if __name__ == "__main__":` block to research different topics.

---

## 📁 Project Structure 
langchain-multi-agent-research-system/
├── app.py # Streamlit UI
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── src/
├── agents/
│ └── agents.py # Search, Reader, Writer, Critic agents
├── tools/
│ └── tools.py # web_search, scrape_url tools
└── Pipelines/
└── pipeline.py # Main research orchestration 

---

## 🔄 Workflow

1. **User Input**: Enter a research topic via the UI
2. **Search Phase**: Search agent queries the web using DuckDuckGo
3. **Reading Phase**: Reader agent extracts content from relevant URLs
4. **Writing Phase**: Writer chain synthesizes findings into a structured report
5. **Review Phase**: Critic chain evaluates the report and provides scores
6. **Output**: Display final report with feedback and scores

---

## 📊 Example Output

The system generates reports with:
- Comprehensive introduction and background
- Key findings with detailed explanations
- Well-sourced conclusions
- Structured sections and proper formatting
- Quality scores from 1-10

---

## 🙏 Acknowledgments

- Built with [LangChain](https://www.langchain.com/)
- Search powered by DuckDuckGo
- UI built with [Streamlit](https://streamlit.io/)
- Inspired by agentic AI research patterns

---

Happy Researching! 🔬