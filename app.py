import streamlit as st
from graph import compiled_graph

st.set_page_config(page_title="Insight Copilot", layout="wide")

# API key from secrets (set in .streamlit/secrets.toml or env var)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
if GROQ_API_KEY:
    import os
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

@st.cache_data
def get_dataset_info():
    from tools import describe_dataset
    return describe_dataset()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar with dataset info
with st.sidebar:
    st.header("Dataset Info")
    info = get_dataset_info()
    st.write(f"Rows: {info['row_count']}")
    st.write(f"Date range: {info['date_range'][0]} to {info['date_range'][1]}")
    st.write(f"Categories: {', '.join(info['categories'])}")
    st.write(f"Regions: {', '.join(info['regions'])}")

# Example question buttons
st.markdown("### Example Questions")
col1, col2, col3, col4 = st.columns(4)
examples = [

    "Seasonal trend in Technology sales",


]
clicked_example = None
for i, (col, ex) in enumerate(zip([col1, col2, col3, col4], examples)):
    if col.button(ex, key=f"example_{i}"):
        clicked_example = ex

# Chat input
user_input = st.chat_input("Ask about sales data...") or clicked_example

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Run agent
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                result = compiled_graph.invoke({
                    "user_query": user_input,
                    "messages": st.session_state.messages[:-1],
                    "plan": None,
                    "tool_results": [],
                    "final_answer": None,
                    "error": None
                })
                answer = result.get("final_answer", "No answer generated.")
            except Exception as e:
                answer = f"Error: {str(e)}"

        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
