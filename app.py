import os
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Insight Copilot",
    layout="wide"
)


# ============================================================
# LOAD GROQ API KEY FROM STREAMLIT SECRETS
# IMPORTANT: This happens BEFORE importing graph
# ============================================================

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    st.error(
        "GROQ_API_KEY is missing. "
        "Please add it in Streamlit Cloud → Manage app → Settings → Secrets."
    )
    st.stop()

os.environ["GROQ_API_KEY"] = GROQ_API_KEY


# ============================================================
# IMPORT GRAPH AFTER API KEY IS SET
# ============================================================

from graph import compiled_graph


# ============================================================
# DATASET INFORMATION
# ============================================================

@st.cache_data
def get_dataset_info():
    from tools import describe_dataset
    return describe_dataset()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Dataset Info")

    try:
        info = get_dataset_info()

        st.write(f"Rows: {info['row_count']}")

        st.write(
            f"Date range: "
            f"{info['date_range'][0]} to "
            f"{info['date_range'][1]}"
        )

        st.write(
            f"Categories: "
            f"{', '.join(info['categories'])}"
        )

        st.write(
            f"Regions: "
            f"{', '.join(info['regions'])}"
        )

    except Exception as e:

        st.error("Could not load dataset information.")

        st.exception(e)


# ============================================================
# TITLE
# ============================================================

st.title("Insight Copilot")

st.write(
    "Ask questions about the sales dataset using natural language."
)


# ============================================================
# EXAMPLE QUESTIONS
# ============================================================

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


# ============================================================
# CHAT INPUT
# ============================================================

user_input = (
    st.chat_input("Ask about sales data...")
    or clicked_example
)


# ============================================================
# DISPLAY PREVIOUS MESSAGES
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# PROCESS USER QUESTION
# ============================================================

if user_input:

    # --------------------------------------------------------
    # Add user message to history
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(user_input)


    # --------------------------------------------------------
    # Run AI agent
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Analyzing sales data..."):

            try:

                result = compiled_graph.invoke(
                    {
                        "user_query": user_input,

                        "messages": (
                            st.session_state.messages[:-1]
                        ),

                        "plan": None,

                        "tool_results": [],

                        "final_answer": None,

                        "error": None
                    }
                )


                # ------------------------------------------------
                # Get final answer
                # ------------------------------------------------

                answer = result.get(
                    "final_answer",
                    "No answer was generated."
                )


                # ------------------------------------------------
                # If graph returned an error
                # ------------------------------------------------

                if result.get("error"):

                    answer = (
                        f"Agent error: "
                        f"{result['error']}"
                    )


            except Exception as e:

                # ------------------------------------------------
                # Show actual error instead of hiding it
                # ------------------------------------------------

                answer = (
                    f"Application error: "
                    f"{type(e).__name__}: {str(e)}"
                )

                st.error("The AI agent encountered an error.")

                st.exception(e)


        # --------------------------------------------------------
        # Display answer
        # --------------------------------------------------------

        st.markdown(answer)


        # --------------------------------------------------------
        # Save assistant response
        # --------------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )