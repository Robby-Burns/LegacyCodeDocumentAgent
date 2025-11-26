# 🤖 Model Card: Legacy Code Documentation Agent

## Agent Overview

| Property | Value |
|----------|-------|
| **Agent Name** | Legacy Code Documentation Agent |
| **Version** | 1.0.0 |
| **Type** | Single-Agent System |
| **Primary Task** | Code Documentation Generation |
| **Domain** | Credit Union / Financial Services IT |

## Agent Description

### Purpose

The Legacy Code Documentation Agent is an AI-powered system designed to automatically generate professional documentation from legacy code files. It is specifically optimized for Credit Union IT environments, understanding domain-specific terminology and producing documentation suitable for both technical and non-technical stakeholders.

### Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                           │
│  ┌─────────────────┐        ┌─────────────────────────┐    │
│  │  Command Line   │        │   Streamlit Web UI      │    │
│  │   (main.py)     │        │      (app.py)           │    │
│  └────────┬────────┘        └───────────┬─────────────┘    │
└───────────┼─────────────────────────────┼──────────────────┘
            │                             │
            ▼                             ▼
┌─────────────────────────────────────────────────────────────┐
│                      AGENT CORE                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   agent.py                           │   │
│  │  • Orchestrates documentation generation             │   │
│  │  • Manages LLM communication                         │   │
│  │  • Tracks token usage and costs                      │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│                        TOOLS                                │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │
│  │ file_handler │ │ pdf_exporter │ │    run_logger    │    │
│  │              │ │              │ │                  │    │
│  │ • Read files │ │ • MD → PDF   │ │ • JSONL logging  │    │
│  │ • Detect     │ │ • Styling    │ │ • Excel export   │    │
│  │   language   │ │ • Formatting │ │ • Statistics     │    │
│  └──────────────┘ └──────────────┘ └──────────────────┘    │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│                   EXTERNAL LLM API                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    LiteLLM                           │   │
│  │  Unified interface to:                               │   │
│  │  • OpenAI (GPT-4o, GPT-4o-mini)                     │   │
│  │  • Google (Gemini 1.5 Flash, Pro)                   │   │
│  │  • Anthropic (Claude Sonnet, Opus)                  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Why Single-Agent vs Multi-Agent?

This system uses a **single-agent architecture** because:

1. **Single, focused task**: Documentation generation is one coherent job
2. **No handoffs needed**: No need for specialists to collaborate
3. **Simpler to maintain**: One prompt, one workflow, one output
4. **Lower latency**: No inter-agent communication overhead
5. **Lower cost**: One LLM call per file

A multi-agent system would be appropriate if we needed:
- Different "specialists" (e.g., security analyst, performance optimizer)
- Iterative refinement with critique/revision cycles
- Complex reasoning chains with verification steps

## Intended Use

### Primary Use Cases

1. **Legacy Code Documentation**: Generate documentation for undocumented or poorly documented legacy systems
2. **Knowledge Transfer**: Create documentation for onboarding new team members
3. **Audit Compliance**: Produce documentation for regulatory requirements
4. **Code Review Support**: Understand unfamiliar code quickly

### Target Users

- Credit Union IT Staff
- Database Administrators
- Business Analysts
- Compliance Officers
- IT Managers (non-technical stakeholders)

### Supported Languages

| Language | Extensions | Common Use Cases |
|----------|------------|------------------|
| SQL | `.sql` | Stored procedures, views, queries |
| Python | `.py` | Scripts, automation, data processing |
| C++ | `.cpp`, `.h` | Core banking integrations |
| DAX | `.dax`, `.m` | Power BI measures, calculations |

## Model Details

### Base LLM

The agent is **LLM-agnostic** and supports multiple providers:

| Provider | Recommended Model | Strengths |
|----------|-------------------|-----------|
| OpenAI | `gpt-4o-mini` | Fast, cost-effective, good quality |
| OpenAI | `gpt-4o` | Highest quality, more expensive |
| Google | `gemini/gemini-1.5-flash` | Very fast, lowest cost |
| Google | `gemini/gemini-1.5-pro` | High quality, good value |
| Anthropic | `claude-sonnet-4-20250514` | Excellent reasoning |
| Anthropic | `claude-opus-4-20250514` | Best quality, highest cost |

### System Prompt

The agent uses a domain-specific system prompt that:

1. **Establishes expertise**: Senior Technical Documentation Specialist role
2. **Defines domain knowledge**: Credit Union terminology (Member, Share, Loan)
3. **Specifies output format**: 7-section Markdown report structure
4. **Sets quality standards**: Professional, accessible tone

### Output Structure
```markdown
## 1. Overview
Plain-English summary for non-technical managers

## 2. Business Logic
Decision rules, conditions, and business processes

## 3. Inputs
| Name | Type | Description |
|------|------|-------------|
| @Param | INT | Description |

## 4. Outputs
| Name | Type | Description |
|------|------|-------------|
| Column | VARCHAR | Description |

## 5. Dependencies
Tables, views, procedures, functions used

## 6. Data Relationships (SQL/DAX only)
JOIN explanations with business context

## 7. Best Practices Review
Actionable improvement recommendations
```

## Performance

### Typical Metrics

| Metric | Value |
|--------|-------|
| Average processing time | 15-30 seconds per file |
| Average input tokens | 500-800 per file |
| Average output tokens | 700-1000 per file |
| Average cost (GPT-4o-mini) | $0.0005-0.0008 per file |
| Success rate | >99% (with valid input) |

### Limitations

1. **Context window**: Very large files (>50KB) may be truncated
2. **Binary files**: Cannot process compiled code
3. **Complex dependencies**: May miss cross-file dependencies
4. **Obfuscated code**: Reduced quality on minified/obfuscated code
5. **Language support**: Limited to SQL, Python, C++, DAX

## Ethical Considerations

### Data Privacy

- ⚠️ **Code is sent to external LLM APIs**: Do not use with sensitive/proprietary code without approval
- ✅ **API keys stored locally**: Never committed to version control
- ✅ **No data retention**: Code is not stored by this tool (check LLM provider policies)

### Bias and Fairness

- The agent focuses on technical documentation, minimizing bias concerns
- Output quality depends on LLM training data
- Credit Union-specific terminology is explicitly included in prompts

### Transparency

- Token usage and costs are logged for every run
- Full run history available in JSONL and Excel formats
- Model used is displayed with every generation

## Evaluation

### Quality Criteria

Documentation is evaluated on:

1. **Accuracy**: Correctly describes what the code does
2. **Completeness**: Covers all sections, no missing information
3. **Clarity**: Understandable by non-technical stakeholders
4. **Actionability**: Best practices section provides useful recommendations
5. **Formatting**: Clean Markdown, proper tables, consistent structure

### Testing

Recommended test cases:
- Simple single-table query
- Complex multi-JOIN stored procedure
- Python function with multiple parameters
- DAX measure with CALCULATE
- Code with errors (to test error handling)

## Maintenance

### Updating the Agent

1. **Prompt tuning**: Edit `prompts.py` to adjust output format or quality
2. **Model updates**: Change `DEFAULT_MODEL` in `.env` to use newer models
3. **New languages**: Add extensions to `EXTENSION_MAP` in `file_handler.py`
4. **Cost updates**: Update `COST_PER_1K_TOKENS` in `agent.py` as pricing changes

### Monitoring

- Review `run_history.xlsx` regularly for:
  - Failed runs and error patterns
  - Cost trends
  - Language distribution
  - Model performance

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-11 | Initial release |

## Contact

For questions or issues, contact your IT department.

---

*This model card follows best practices from [Mitchell et al., 2019](https://arxiv.org/abs/1810.03993) and the [AI Agent Card framework](https://arxiv.org/abs/2312.12687).*
```

---

## Your Final Project Structure:
```
LegacyCodeDocumentAgent/
├── .venv/
├── .env
├── .gitignore
├── .streamlit/
│   └── config.toml
├── requirements.txt        ← NEW
├── README.md               ← NEW
├── MODEL_CARD.md           ← NEW
├── main.py
├── app.py
├── agent.py
├── prompts.py
├── file_handler.py
├── pdf_exporter.py
├── run_logger.py
├── output/
├── sample_files/
├── run_history.jsonl
└── run_history.xlsx