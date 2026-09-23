Insight Copilot - Sales Data Analysis Agent

An AI-powered sales data analysis assistant built using Python, LangGraph, Groq, Streamlit, Pandas, and OpenPyXL.

Insight Copilot allows users to ask natural-language questions about a sales dataset and receive analytical answers through an agentic workflow.

Live Demo

Streamlit Cloud:

https://vedn25-insight-copilot-sales-data-analysis-jbwapp565ycdzhqrkxq.streamlit.app/

GitHub Repository

https://github.com/VedN25/VedN25-Insight-Copilot-Sales-data-analysis

Project Overview

Insight Copilot is a conversational AI application designed to analyze structured sales data using natural-language queries.

Instead of manually filtering spreadsheets or writing data-analysis queries, users can ask questions such as:

Which category has the highest sales?

Tell me about the sales data

Seasonal trend in Technology sales

The application processes the user's question through a LangGraph-based agent workflow, uses data-analysis tools to retrieve information from the sales dataset, and generates a natural-language response.

Key Features

Natural-language sales data analysis

LangGraph-based agent workflow

Excel dataset analysis

Pandas-based data processing

Interactive Streamlit interface

Example questions for quick testing

Dataset information displayed in the sidebar

Conversation history

Error handling

Secure API key management using Streamlit Secrets

Public Streamlit Cloud deployment

Technology Stack

Technology

Purpose

Python

Core programming language

LangGraph

Agent workflow orchestration

Groq

LLM inference

OpenAI Python Client

LLM API client

Pandas

Data processing

OpenPyXL

Excel file handling

Plotly

Data visualization

Streamlit

Web interface

Pytest

Testing

Git/GitHub

Version control

Streamlit Cloud

Deployment

Architecture

                    User
                      |
                      v
             Streamlit Interface
                      |
                      v
                 User Query
                      |
                      v
               LangGraph Agent
                      |
             +--------+--------+
             |                 |
             v                 v
          Planner         Data Tools
                               |
                               v
                       Sales Dataset
                       Excel File
                               |
                               v
                       Analysis Results
             |                 |
             +--------+--------+
                      |
                      v
                Final Answer
                      |
                      v
              Streamlit Interface

Agent Workflow

The application uses LangGraph to organize the agent workflow.

User Question
      |
      v
Planning
      |
      v
Determine Required Analysis
      |
      v
Execute Data Analysis Tools
      |
      v
Process Results
      |
      v
Generate Final Answer
      |
      v
Display Answer

This approach separates the reasoning process from the underlying deterministic data-analysis operations.

Dataset

The application uses:

data/Sales_Dataset_2024.xlsx

The dataset is loaded using Pandas and OpenPyXL.

The application can retrieve information such as:

Number of rows

Date range

Product categories

Regions

Sales information

Dataset information is displayed in the Streamlit sidebar.

Example Questions

The application provides three example questions for quick testing:

Which category has the highest sales?

Tell me about the sales data

Seasonal trend in Technology sales

Users can also enter their own questions through the chat input.

Project Structure

VedN25-Insight-Copilot-Sales-data-analysis/
│
├── data/
│   ├── Sales_Dataset_2024.xlsx
│   ├── __init__.py
│   └── loader.py
│
├── .streamlit/
│   └── secrets.toml.example
│
├── app.py
├── graph.py
├── tools.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example

File Descriptions

app.py

Main Streamlit application responsible for:

Streamlit UI

API key loading

Dataset information

Example questions

Chat interface

Agent execution

Response display

Error handling

graph.py

Contains the LangGraph agent workflow, including:

Agent state

Planning

Tool execution

Workflow orchestration

Final answer generation

tools.py

Contains the data-analysis tools used by the agent to interact with the sales dataset.

data/loader.py

Responsible for loading and preparing the sales dataset.

data/Sales_Dataset_2024.xlsx

The primary sales dataset used by the application.

requirements.txt

Contains the Python dependencies required to run the project.

Installation

1. Clone the Repository

git clone https://github.com/VedN25/VedN25-Insight-Copilot-Sales-data-analysis.git

Move into the project directory:

cd VedN25-Insight-Copilot-Sales-data-analysis

2. Create a Virtual Environment

Windows

python -m venv .venv
.venv\Scripts\activate

macOS/Linux

python3 -m venv .venv
source .venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

API Key Configuration

The application requires a Groq API key.

For local development, configure the environment variable:

GROQ_API_KEY=your_api_key_here

Do not commit your real API key to GitHub.

Streamlit Cloud Secrets

For Streamlit Cloud deployment, add the API key under:

Streamlit Cloud -> App Settings -> Secrets

Use:

GROQ_API_KEY = "your_actual_api_key"

The application reads the secret using:

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

The actual API key is never stored in the GitHub repository.

Running Locally

After activating the virtual environment and installing dependencies:

python -m streamlit run app.py

The application will normally be available at:

http://localhost:8501

Deployment

The application is deployed using Streamlit Community Cloud.

Deployment workflow:

GitHub Repository
       |
       v
Streamlit Cloud
       |
       v
Install requirements.txt
       |
       v
Load Streamlit Secrets
       |
       v
Run app.py
       |
       v
Public Application

Live Application

https://vedn25-insight-copilot-sales-data-analysis-jbwapp565ycdzhqrkxq.streamlit.app/

The deployed application should be tested using an incognito/private browser window before submission.

Security

The following files and directories should not be committed:

.env
.streamlit/secrets.toml
__pycache__/
*.pyc
.pytest_cache/
.venv/
venv/

API keys are stored through Streamlit Secrets rather than hard-coded into the application.

.gitignore

The project uses .gitignore to prevent sensitive credentials and generated files from being committed.

.env
.streamlit/secrets.toml
__pycache__/
*.pyc
.pytest_cache/
.venv/
venv/

Pytest Cache

The .pytest_cache/ directory contains data generated by pytest's cache plugin.

It provides functionality for options such as:

--lf

--ff

cache fixture

The .pytest_cache/ directory should not be committed to version control.

For more information, see the official pytest documentation:

https://docs.pytest.org/en/stable/how-to/cache.html

Testing

The project includes Pytest dependencies.

Run tests using:

pytest

For detailed output:

pytest -v

Dependency Versions

The project uses pinned dependency versions for more predictable deployments.

langgraph==0.2.34
openai==1.35.0
httpx==0.27.2
pandas==2.2.3
openpyxl==3.1.5
plotly==5.24.1
streamlit==1.39.0
pytest==8.3.3
pytest-asyncio==0.23.8

The httpx version is explicitly pinned to maintain compatibility with the selected OpenAI client version.

Example Workflow

For a question such as:

Which category has the highest sales?

the application follows this process:

1. User enters the question
        |
        v
2. LangGraph receives the query
        |
        v
3. Agent determines the required analysis
        |
        v
4. Relevant data-analysis tool is executed
        |
        v
5. Sales data is analyzed
        |
        v
6. Result is passed to the response generation step
        |
        v
7. Natural-language answer is displayed

Design Decisions

Why LangGraph?

LangGraph provides a structured framework for building agent workflows.

It allows the application to separate planning, tool execution, and response generation instead of placing all logic into a single function.

Why Pandas?

Pandas provides efficient operations for structured tabular data.

It is used for:

Data loading

Filtering

Grouping

Aggregation

Statistical calculations

Date-based analysis

Why Streamlit?

Streamlit provides a simple way to build an interactive interface around the AI agent without requiring a separate frontend framework.

Why Groq?

Groq provides fast LLM inference, making it suitable for an interactive data-analysis application.

Error Handling

The application includes error handling for:

Missing API credentials

Dataset loading errors

Agent execution errors

API errors

Unexpected runtime errors

Errors are displayed in the Streamlit interface without terminating the complete application.

Conversation Handling

The Streamlit application maintains conversation history for display.

For agent execution, the application avoids unnecessarily sending the complete previous conversation history to the LLM.

This helps reduce unnecessarily large LLM requests and lowers the risk of exceeding message or completion limits.

Future Improvements

Potential improvements include:

Additional sales-analysis tools

Automatic chart generation

More advanced visualizations

Query classification

Improved conversation memory

Larger dataset support

Automated agent evaluation

More comprehensive unit tests

Response quality evaluation

Authentication

Better caching

Advanced analytics and forecasting

Internship Submission

Hosted Application

https://vedn25-insight-copilot-sales-data-analysis-jbwapp565ycdzhqrkxq.streamlit.app/

GitHub Repository

https://github.com/VedN25/VedN25-Insight-Copilot-Sales-data-analysis

Short Write-up

Insight Copilot is an agentic AI application that allows users to analyze sales data using natural-language questions. The system uses LangGraph to orchestrate the agent workflow, Groq for LLM inference, Pandas and OpenPyXL for structured data processing, and Streamlit for the user interface.

The main design decision was to combine an LLM-based agent with deterministic data-analysis tools. This allows the system to use natural language for understanding the user's intent while relying on the actual sales dataset for analytical results.

The application is deployed on Streamlit Cloud and uses Streamlit Secrets to securely manage the Groq API key.