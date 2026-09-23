import os
import streamlit as st

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Insight Copilot",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# Load API key from Streamlit Secrets
# ---------------------------------------------------------
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if GROQ_API_KEY:
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY


# ---------------------------------------------------------
# Import agent
# ---------------------------------------------------------
from graph import compiled_graph


# ---------------------------------------------------------
# Dataset information
# ---------------------------------------------------------
@st.cache_data
def get_dataset_info():
    from tools import describe_dataset
    return describe_dataset()


# ---------------------------------------------------------
# Initialize session state
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# Title
# ---------------------------------------------------------
st.title("Insight Copilot")

st.write(
    "Ask questions about the sales dataset using natural language."
)


# ---------------------------------------------------------
# Sidebar - Dataset information
# ---------------------------------------------------------
with st.sidebar:

    st.header("Dataset Info")

    try:
        info = get_dataset_info()

        st.write(f"Rows: {info['row_count']}")

        st.write(
            f"Date range: "
            f"{info['date_range'][0]} to {info['date_range'][1]}"
        )

        st.write(
            f"Categories: {', '.join(info['categories'])}"
        )

        st.write(
            f"Regions: {', '.join(info['regions'])}"
        )

    except Exception as e:

        st.error("Unable to load dataset information.")

        st.exception(e)


# ---------------------------------------------------------
# Example questions
# ---------------------------------------------------------
st.markdown("### Example Questions")

col1, col2, col3, col4 = st.columns(4)

examples = [
    "Seasonal trend in Technology sales",
    "Tell me about the sales data",
    "Which category has the highest sales?",
    "What are the regional sales trends?"
]

clicked_example = None

for i, (col, example) in enumerate(
    zip(
        [col1, col2, col3, col4],
        examples
    )
):

    if col.button(
        example,
        key=f"example_{i}",
        use_container_width=True
    ):
        clicked_example = example


# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------
user_input = (
    st.chat_input("Ask about sales data...")
    or clicked_example
)


# ---------------------------------------------------------
# Display previous conversation
# ---------------------------------------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------------------------------------------------------
# Process user question
# ---------------------------------------------------------
if user_input:

    # Add user message to UI history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Display user message
    with st.chat_message("user"):

        st.markdown(user_input)


    # -----------------------------------------------------
    # Run LangGraph agent
    # -----------------------------------------------------
    with st.chat_message("assistant"):

        with st.spinner("Analyzing sales data..."):

            try:

                result = compiled_graph.invoke(
                    {
                        "user_query": user_input,

                        # IMPORTANT:
                        # Do not send the entire Streamlit
                        # conversation history to the LLM.
                        "messages": [],

                        "plan": None,

                        "tool_results": [],

                        "final_answer": None,

                        "error": None
                    }
                )

                answer = result.get(
                    "final_answer",
                    "No answer generated."
                )

                if not answer:
                    answer = "No answer was generated."


            except Exception as e:

                answer = f"Error generating answer: {str(e)}"


        # Display answer
        st.markdown(answer)


        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )