# Insight Copilot - Sales Analytics Agent

A LangGraph-based AI agent for sales data analysis with natural language queries, automatic chart generation, and conversational memory.

## Features

- **Natural Language Queries**: Ask questions about sales data in plain English
- **Automatic Visualization**: Generates Plotly charts (bar, line, scatter, area) based on query intent
- **Conversational Memory**: Remembers context for follow-up questions
- **Safe Data Access**: Constrained pandas queries with column whitelisting
- **Multi-step Reasoning**: Planner → Tool Execution → Synthesizer architecture

## Architecture

```
User Question
     ↓
┌──────────┐
│   Planner   │  ← LLM creates execution plan
└──────────┘
       ↓
┌──────────┐
│    Tools    │  ← Execute: query_data, compute_stats, make_chart, describe_dataset
└──────────┘
       ↓
┌──────────┐
│ Synthesizer │  ← LLM generates natural language answer
└──────────┘
       ↓
   Answer + Chart
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Copy the example secrets file and add your Groq API key:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml and add your GROQ_API_KEY
```

Or set as environment variable:
```bash
set GROQ_API_KEY=your-key-here   # Windows PowerShell
# or
export GROQ_API_KEY=your-key-here   # Linux/macOS
```

### 3. Run the App

```bash
streamlit run app.py
```

## Example Questions

- "What are the total sales by region?"
- "Show me top 5 products by revenue"
- "Sales trend over time"
- "Which region has highest profit margin?"
- "Compare sales across categories"
- "Growth rate of revenue by quarter"
- "Top salesperson by units sold"
- "Show me the dataset schema"

## Project Structure

```
xcaliber-assignment/
├── app.py                 # Streamlit chat interface
├── graph.py               # LangGraph agent (Planner → Tools → Synthesizer)
├── tools.py               # Tool implementations (query_data, make_chart, describe_dataset, compute_stats)
├── data/
│   └── loader.py          # Dataset loading (CSV or Excel)
├── .streamlit/
│   ├── secrets.toml.example
│   └── config.toml
├── requirements.txt
├── .gitignore
└── README.md
```

## Dataset

The agent works with a sales dataset provided as either:
- `data/global_superstore.csv` (legacy format)
- `data/Sales_Dataset_2024.xlsx` (current format)

The loader (`data/loader.py`) reads whichever file exists. The current Excel format contains columns:
- `Date` (datetime)
- `Region` (string): North, South, East, West
- `Product` (string)
- `Salesperson` (string)
- `Units_Sold` (int)
- `Unit_Price` (float)
- `Category` (string): Electronics, Accessories, Office
- `Revenue` (float)
- `Cost` (float)
- `Profit` (float)

## Tools

| Tool | Description |
|------|-------------|
| `describe_dataset` | Explore schema, columns, date ranges, unique values |
| `query_data` | Filter, group, aggregate with pandas (supports date_range, compare, time_granularity, top_n, limit) |
| `compute_stats` | Sum, mean, median, growth_rate, top_n, etc. on previous query results |
| `make_chart` | Generate Plotly bar, line, scatter, area charts (returns DataFrame ready for `st.bar_chart`) |

## LLM Configuration

- **Provider**: Groq
- **Model**: `openai/gpt-oss-120b`
- **Features**: JSON mode for structured planning, retry logic with exponential backoff

## Testing

```bash
# Run tool tests (if test file exists)
python -m pytest tests/ -v

# Quick sanity check of the agent graph
python graph.py
```

## Deployment

### Streamlit Cloud

1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add `GROQ_API_KEY` in Settings → Secrets
4. Deploy

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## License

MIT License - Built for Gen AI Internship Take-Home Assignment
﻿# Insight Copilot - Sales Analytics Agent

A LangGraph-based AI agent for sales data analysis with natural language queries, automatic chart generation, and conversational memory.

## Features

- **Natural Language Queries**: Ask questions about sales data in plain English
- **Automatic Visualization**: Generates Plotly charts (bar, line, scatter, area) based on query intent
- **Conversational Memory**: Remembers context for follow-up questions
- **Safe Data Access**: Constrained pandas queries with column whitelisting
- **Multi-step Reasoning**: Planner → Tool Execution → Synthesizer architecture

## Architecture

`
User Question
     ↓
┌────────────┐
│   Planner   │  ← LLM creates execution plan
└────────────┘
       ↓
┌────────────┐
│    Tools    │  ← Execute: query_data, compute_stats, make_chart, describe_dataset
└────────────┘
       ↓
┌────────────┐
│ Synthesizer │  ← LLM generates natural language answer
└────────────┘
       ↓
   Answer + Chart
`

## Quick Start

### 1. Install Dependencies

`ash
pip install -r requirements.txt
`

### 2. Configure API Key

Copy the example secrets file and add your Groq API key:

`ash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml and add your GROQ_API_KEY
`

Or set as environment variable:
`ash
set GROQ_API_KEY=your-key-here   # Windows PowerShell
# or
export GROQ_API_KEY=your-key-here   # Linux/macOS
`

### 3. Run the App

`ash
streamlit run app.py
`

## Example Questions

-  What are the total sales by region?
- Show me top 5 products by revenue
- Sales trend over time
- Which region has highest profit margin?
- Compare sales across categories
- Growth rate of revenue by quarter
- Top salesperson by units sold
- Show me the dataset schema

## Project Structure

`
xcaliber-assignment/
├── app.py                 # Streamlit chat interface
├── graph.py               # LangGraph agent (Planner → Tools → Synthesizer)
├── tools.py               # Tool implementations (query_data, make_chart, describe_dataset, compute_stats)
├── data/
│   └── loader.py          # Dataset loading (CSV or Excel)
├── .streamlit/
│   ├── secrets.toml.example
│   └── config.toml
├── requirements.txt
├── .gitignore
└── README.md
`

## Dataset

The agent works with a sales dataset provided as either:
- data/global_superstore.csv (legacy format)
- data/Sales_Dataset_2024.xlsx (current format)

The loader (data/loader.py) reads whichever file exists. The current Excel format contains columns:
- Date (datetime)
- Region (string): North, South, East, West
- Product (string)
- Salesperson (string)
- Units_Sold (int)
- Unit_Price (float)
- Category (string): Electronics, Accessories, Office
- Revenue (float)
- Cost (float)
- Profit (float)

## Tools

| Tool | Description |
|------|-------------|
| describe_dataset | Explore schema, columns, date ranges, unique values |
| query_data | Filter, group, aggregate with pandas (supports date_range, compare, time_granularity, top_n, limit) |
| compute_stats | Sum, mean, median, growth_rate, top_n, etc. on previous query results |
| make_chart | Generate Plotly bar, line, scatter, area charts (returns DataFrame ready for st.bar_chart) |

## LLM Configuration

- **Provider**: Groq
- **Model**: openai/gpt-oss-120b
- **Features**: JSON mode for structured planning, retry logic with exponential backoff

## Testing

`ash
# Run tool tests (if test file exists)
python -m pytest tests/ -v

# Quick sanity check of the agent graph
python graph.py
`

## Deployment

### Streamlit Cloud

1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add GROQ_API_KEY in Settings → Secrets
4. Deploy

### Docker

`dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD [streamlit, run, app.py, --server.port=8501, --server.address=0.0.0.0]
`

## License

MIT License - Built for Gen AI Internship Take-Home Assignment
