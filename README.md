# 📄 Legacy Code Documentation Agent

AI-powered tool that automatically generates professional documentation from legacy code files. Built for Credit Union IT teams.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![LLM](https://img.shields.io/badge/LLM-Agnostic-purple.svg)](#available-models)
[![Demo](https://img.shields.io/badge/🤗%20Live%20Demo-Hugging%20Face-yellow)](https://huggingface.co/spaces/Rob200/LegacyCodeDocumentAgent)

## 🎮 [Try the Live Demo →](https://huggingface.co/spaces/Rob200/LegacyCodeDocumentAgent)

---

## The Problem

| Challenge | Business Impact |
|-----------|-----------------|
| Undocumented legacy code | 40% of developer time spent understanding existing code |
| Knowledge silos | Critical logic trapped in senior employees' heads |
| Compliance gaps | Auditors require documentation that doesn't exist |
| Slow onboarding | New hires take 3-6 months to become productive |

## The Solution

This agent reads SQL, Python, C++, and DAX files and generates standardized 7-section documentation in seconds.

| Metric | Manual | With Agent | Improvement |
|--------|--------|------------|-------------|
| Time per file | 30-60 min | 30 sec | **98% faster** |
| Cost per file | ~$25 | $0.001 | **99.99% cheaper** |
| Consistency | Varies | Standardized | **100% consistent** |

---

## Features

- 🔍 **Multi-language**: SQL, Python, C++, DAX
- 🏦 **Domain-aware**: Credit Union terminology (Member, Loan, Share)
- 📊 **7-section reports**: Overview, Business Logic, Inputs, Outputs, Dependencies, Data Relationships, Best Practices
- 📄 **Export formats**: Markdown + PDF
- 💰 **Cost tracking**: Token usage and API costs logged to Excel
- 📁 **Batch processing**: Document entire folders
- 🔄 **LLM-agnostic**: OpenAI, Google Gemini, or Anthropic Claude

---

## Quick Start
```bash
# Clone and setup
git clone https://github.com/Robby-Burns/LegacyCodeDocumentAgent.git
cd LegacyCodeDocumentAgent
python -m venv .venv && .venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env with your OPENAI_API_KEY

# Run
streamlit run app.py           # Web UI
python main.py code.sql --pdf  # Command line
```

---

## Sample Output
```markdown
## 1. Overview
Retrieves members with overdue loan payments, filtered by days and loan type.

## 2. Business Logic
- Identifies loans past due by specified threshold
- Filters to active accounts only
- Optional loan type filtering

## 3. Inputs
| Name | Type | Description |
|------|------|-------------|
| @DaysOverdue | INT | Days past due threshold (default: 30) |

## 4-7. [Outputs, Dependencies, Data Relationships, Best Practices...]
```

---

## Architecture
```
┌──────────────────────────────────────────────────────┐
│                   USER INTERFACE                     │
│     Command Line (main.py)  │  Streamlit (app.py)   │
└──────────────────┬───────────────────────────────────┘
                   ▼
┌──────────────────────────────────────────────────────┐
│                    AGENT CORE                        │
│  file_handler → agent.py → pdf_exporter/run_logger  │
└──────────────────┬───────────────────────────────────┘
                   ▼
┌──────────────────────────────────────────────────────┐
│              LiteLLM (LLM-Agnostic API)              │
│       OpenAI  │  Google Gemini  │  Anthropic        │
└──────────────────────────────────────────────────────┘
```

---

## Production Roadmap

This POC validates the core value. Production deployment would add:

| Phase | Enhancements |
|-------|--------------|
| **Security** | On-premise LLM, PII redaction, NCUA/SOC2 audit logging, AD/LDAP integration |
| **Scale** | Git/Azure DevOps integration, CI/CD hooks, Redis job queue, caching |
| **Features** | Multi-file context, version comparison, custom templates, code quality scoring |

---

## Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| LLM Interface | LiteLLM | Provider-agnostic, swap models without code changes |
| Web UI | Streamlit | Rapid prototyping, Python-native |
| PDF Export | FPDF2 | Pure Python, no system dependencies |
| Logging | JSONL + Excel | Append-only reliability, Excel for stakeholders |

---

## Project Structure
```
├── main.py           # CLI interface
├── app.py            # Streamlit web UI
├── agent.py          # LLM communication + cost tracking
├── prompts.py        # System prompts
├── file_handler.py   # File reading + language detection
├── pdf_exporter.py   # Markdown → PDF
├── run_logger.py     # JSONL + Excel logging
└── output/           # Generated documentation
```

---

## Author

**Robby Burns** — AI/ML Product Manager

[🌐 Website](https://robby-burns-about-me.vercel.app/) • [💼 LinkedIn](www.linkedin.com/in/robert-burns-mba-mds-ms-pmp-1a04531a9) • [🐙 GitHub](https://github.com/Robby-Burns)

---

## License

MIT License — See [LICENSE](LICENSE) for details.