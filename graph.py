"""LangGraph agent for Insight Copilot."""

import json
import time
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from openai import OpenAI
import os

from tools import query_data, make_chart, describe_dataset, compute_stats


def _get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set")
    return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")


class AgentState(TypedDict):
    user_query: str
    messages: List[Dict[str, str]]
    plan: Optional[Dict[str, Any]]
    tool_results: List[Dict[str, Any]]
    final_answer: Optional[str]
    error: Optional[str]


TOOLS = {
    "query_data": query_data,
    "make_chart": make_chart,
    "describe_dataset": describe_dataset,
    "compute_stats": compute_stats,
}


def _call_groq_with_retry(messages, max_retries=2, json_mode=False):
    client = _get_client()
    for attempt in range(max_retries + 1):
        try:
            kwargs = {
                "model": "openai/gpt-oss-120b",
                "messages": messages,
                "temperature": 0.1,
            }
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}
            response = client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            if attempt < max_retries and ("rate_limit" in str(e).lower() or "timeout" in str(e).lower()):
                time.sleep(2)
                continue
            raise
def planner_node(state):
    system_prompt = """You are a planner for a sales data analysis agent.
Given a user question, output a JSON plan with:
- "reasoning": brief explanation of approach
- "needs_tools": boolean
- "tool_calls": list of {"tool": str, "args": dict} (empty if needs_tools=false)
- "if_no_tool_reason": str (required if needs_tools=false)

Available tools:
1. query_data(filter_spec: dict) - filter, group, aggregate data. filter_spec keys: column, operator, value, groupby, agg, agg_column, top_n, date_range, compare, time_granularity, limit
   - operator MUST be one of: ==, !=, >, <, >=, <=, in, not in
   - Use == for equality (NOT =)
   - For time series: groupby "Date" gives daily (365 rows). For seasonal trends, use time_granularity: "month" (or "week"/"quarter"/"year") to aggregate by time period, OR use date_range + limit to restrict rows
   - time_granularity: "month", "week", "quarter", "year" - converts Date to period before grouping
   - limit: int - explicitly limit number of rows returned
2. make_chart(data: pd.DataFrame, x: str, y: str) - returns DataFrame for bar chart
   - For data, use "RESULT_OF_PREVIOUS_CALL" to reference the previous tool's result
3. describe_dataset() - returns dataset metadata
4. compute_stats(data: list, operations: list) - compute statistics on data. operations: list of {"operation": "sum|mean|min|max|count|std", "column": "col_name"}
   - For data, use "RESULT_OF_PREVIOUS_CALL" to reference the previous tool's result (must be a query_data result)

Dataset columns (use EXACT names):
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

Category mapping: "Technology" or "Tech" -> "Electronics"

Only use tools that exist. Validate column names against dataset schema above.
Output ONLY valid JSON. The response must be in json format."""
    user_prompt = f"User question: {state['user_query']}\n\nConversation history: {state.get('messages', [])}\n\nRespond with valid json. Output must be a json object."
    try:
        response = _call_groq_with_retry([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ], json_mode=True)
        plan = json.loads(response)
        if "needs_tools" not in plan: plan["needs_tools"] = False
        if "tool_calls" not in plan: plan["tool_calls"] = []
        if "reasoning" not in plan: plan["reasoning"] = ""
        if not plan["needs_tools"] and "if_no_tool_reason" not in plan:
            plan["if_no_tool_reason"] = "No tools needed"
        state["plan"] = plan
        state["error"] = None
    except Exception as e:
        state["error"] = f"Planner failed: {str(e)}"
        state["plan"] = {"reasoning": "", "needs_tools": False, "tool_calls": [], "if_no_tool_reason": "Planner error"}
    return state


def tool_executor_node(state):
    tool_results = []
    plan = state.get("plan", {})
    previous_result = None
    for tool_call in plan.get("tool_calls", []):
        tool_name = tool_call.get("tool")
        args = tool_call.get("args", {})
        if tool_name not in TOOLS:
            tool_results.append({"tool": tool_name, "args": args, "error": f"Unknown tool: {tool_name}"})
            continue
        try:
            # Handle RESULT_OF_PREVIOUS_CALL reference
            if "data" in args and args["data"] == "RESULT_OF_PREVIOUS_CALL":
                if previous_result is not None:
                    args = args.copy()
                    args["data"] = previous_result
                else:
                    tool_results.append({"tool": tool_name, "args": args, "error": "No previous result to reference"})
                    continue
            result = TOOLS[tool_name](**args)
            if hasattr(result, "to_dict"):
                result = result.to_dict(orient="records")
            tool_results.append({"tool": tool_name, "args": args, "result": result})
            previous_result = result
        except Exception as e:
            tool_results.append({"tool": tool_name, "args": args, "error": str(e)})
    state["tool_results"] = tool_results
    return state


def synthesizer_node(state):
    if state.get("error"):
        state["final_answer"] = "I'm temporarily unavailable — please try again in a moment."
        return state
    system_prompt = """You are a sales data analyst. Given the user question, the plan reasoning, and tool results, produce a concise answer in this format:

1. If there are numerical results: a markdown table with the key numbers
2. One direct-answer sentence answering the user's question
3. One "What stands out:" sentence with an insight

Do NOT dump raw data. Do NOT include reasoning. Be concise and business-focused.
IMPORTANT: You are NOT allowed to call any tools. Only output the final answer text."""
    tool_results_summary = json.dumps(state.get("tool_results", []), default=str)
    plan_reasoning = state.get("plan", {}).get("reasoning", "")
    user_prompt = f"""Question: {state['user_query']}
Plan reasoning: {plan_reasoning}
Tool results: {tool_results_summary}"""
    try:
        response = _call_groq_with_retry([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        state["final_answer"] = response
    except Exception as e:
        state["final_answer"] = f"Error generating answer: {str(e)}"
    return state


def should_use_tools(state):
    if state.get("error"):
        return "synthesizer"
    plan = state.get("plan", {})
    return "tool_executor" if plan.get("needs_tools", False) else "synthesizer"


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("planner", planner_node)
    graph.add_node("tool_executor", tool_executor_node)
    graph.add_node("synthesizer", synthesizer_node)
    graph.set_entry_point("planner")
    graph.add_conditional_edges("planner", should_use_tools, {
        "tool_executor": "tool_executor",
        "synthesizer": "synthesizer"
    })
    graph.add_edge("tool_executor", "synthesizer")
    graph.add_edge("synthesizer", END)
    return graph.compile()


compiled_graph = build_graph()
