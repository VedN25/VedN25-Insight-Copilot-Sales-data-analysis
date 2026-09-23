"""Tools for Insight Copilot agent — unified exports with simplified signatures."""

import pandas as pd
from data.loader import load_dataset

# Load dataset once at module level
_df = load_dataset()


def _validate_column(col: str, context: str = "column") -> None:
    """Validate column exists in dataframe."""
    if col not in _df.columns:
        raise ValueError(f"Invalid {context}: '{col}'. Must be one of: {list(_df.columns)}")


def query_data(filter_spec: dict) -> pd.DataFrame:
    """
    Query the dataset with filtering, grouping, and aggregation.

    filter_spec keys:
    - column: str - column to filter on
    - operator: str - one of ==, !=, >, <, >=, <=, in, not in
    - value: any - value to filter by
    - groupby: str (optional) - column to group by
    - agg: str (optional) - aggregation: sum, mean, count, min, max
    - agg_column: str (optional) - column to aggregate
    - top_n: int (optional) - return top N rows by agg_column
    - date_range: tuple (optional) - (start_date, end_date) for Order Date
    - compare: dict (optional) - {"column": "Region", "values": ["A", "B"]} for comparisons
    - time_granularity: str (optional) - "month", "week", "quarter", "year" for time-based grouping
    - limit: int (optional) - limit number of rows returned
    """
    df = _df.copy()

    # Date range filter
    if filter_spec.get("date_range"):
        start, end = filter_spec["date_range"]
        df = df[(df["Date"] >= pd.Timestamp(start)) & (df["Date"] <= pd.Timestamp(end))]

    # Comparison filter (e.g., compare Region A vs Region B)
    if filter_spec.get("compare"):
        comp = filter_spec["compare"]
        _validate_column(comp["column"], "compare column")
        df = df[df[comp["column"]].isin(comp["values"])]

    # Regular column filter
    if filter_spec.get("column"):
        _validate_column(filter_spec["column"], "filter column")
        col = filter_spec["column"]
        op = filter_spec.get("operator", "==")
        val = filter_spec.get("value")

        if op == "==":
            df = df[df[col] == val]
        elif op == "!=":
            df = df[df[col] != val]
        elif op == ">":
            df = df[df[col] > val]
        elif op == ">=":
            df = df[df[col] >= val]
        elif op == "<":
            df = df[df[col] < val]
        elif op == "<=":
            df = df[df[col] <= val]
        elif op == "in":
            df = df[df[col].isin(val)]
        elif op == "not in":
            df = df[~df[col].isin(val)]
        else:
            raise ValueError(f"Unsupported operator: {op}")

    # Time granularity for date grouping (month, week, quarter, year)
    if filter_spec.get("time_granularity"):
        granularity = filter_spec["time_granularity"]
        if granularity == "month":
            df["Date"] = df["Date"].dt.to_period("M").dt.to_timestamp()
        elif granularity == "week":
            df["Date"] = df["Date"].dt.to_period("W").dt.to_timestamp()
        elif granularity == "quarter":
            df["Date"] = df["Date"].dt.to_period("Q").dt.to_timestamp()
        elif granularity == "year":
            df["Date"] = df["Date"].dt.to_period("Y").dt.to_timestamp()
        else:
            raise ValueError(f"Unsupported time_granularity: {granularity}")

    # Groupby and aggregation
    if filter_spec.get("groupby"):
        _validate_column(filter_spec["groupby"], "groupby column")
        groupby_col = filter_spec["groupby"]

        if filter_spec.get("agg") and filter_spec.get("agg_column"):
            _validate_column(filter_spec["agg_column"], "aggregation column")
            agg_col = filter_spec["agg_column"]
            agg_func = filter_spec["agg"]

            if agg_func == "sum":
                df = df.groupby(groupby_col)[agg_col].sum().reset_index()
            elif agg_func == "mean":
                df = df.groupby(groupby_col)[agg_col].mean().reset_index()
            elif agg_func == "count":
                df = df.groupby(groupby_col)[agg_col].count().reset_index()
            elif agg_func == "min":
                df = df.groupby(groupby_col)[agg_col].min().reset_index()
            elif agg_func == "max":
                df = df.groupby(groupby_col)[agg_col].max().reset_index()
            else:
                raise ValueError(f"Unsupported aggregation: {agg_func}")
        else:
            df = df.groupby(groupby_col).size().reset_index(name="count")

    # Top-N
    if filter_spec.get("top_n") and filter_spec.get("agg_column"):
        df = df.nlargest(filter_spec["top_n"], filter_spec["agg_column"])

    # Limit
    if filter_spec.get("limit"):
        df = df.head(filter_spec["limit"])

    # Default limit if no aggregation/groupby and no explicit limit
    if not filter_spec.get("groupby") and not filter_spec.get("agg") and not filter_spec.get("limit"):
        df = df.head(10)

    return df


def make_chart(data: pd.DataFrame, x: str, y: str) -> pd.DataFrame:
    """Return DataFrame indexed by x with column y for st.bar_chart()."""
    if x not in data.columns or y not in data.columns:
        raise ValueError(f"Columns must exist in data. Got x='{x}', y='{y}', available: {list(data.columns)}")
    return data.set_index(x)[[y]]


def describe_dataset() -> dict:
    """Return dataset metadata."""
    return {
        "columns": list(_df.columns),
        "dtypes": {col: str(dtype) for col, dtype in _df.dtypes.items()},
        "row_count": int(len(_df)),
        "date_range": [
            _df["Date"].min().strftime("%Y-%m-%d"),
            _df["Date"].max().strftime("%Y-%m-%d")
        ],
        "categories": sorted(_df["Category"].dropna().astype(str).unique().tolist()),
        "regions": sorted(_df["Region"].dropna().astype(str).unique().tolist())
    }


def compute_stats(data: list, operations: list) -> dict:
    """
    Compute statistics on provided data.

    operations: list of dicts with keys:
    - operation: str - one of sum, mean, min, max, count, std
    - column: str - column name to compute on
    """
    df = pd.DataFrame(data)
    results = {}
    for op in operations:
        operation = op.get("operation")
        column = op.get("column")
        if column not in df.columns:
            results[f"{operation}_{column}"] = f"Column '{column}' not found"
            continue
        try:
            if operation == "sum":
                results[f"{operation}_{column}"] = float(df[column].sum())
            elif operation == "mean":
                results[f"{operation}_{column}"] = float(df[column].mean())
            elif operation == "min":
                results[f"{operation}_{column}"] = float(df[column].min())
            elif operation == "max":
                results[f"{operation}_{column}"] = float(df[column].max())
            elif operation == "count":
                results[f"{operation}_{column}"] = int(df[column].count())
            elif operation == "std":
                results[f"{operation}_{column}"] = float(df[column].std())
            else:
                results[f"{operation}_{column}"] = f"Unsupported operation: {operation}"
        except Exception as e:
            results[f"{operation}_{column}"] = f"Error: {str(e)}"
    return results


__all__ = ["query_data", "make_chart", "describe_dataset", "compute_stats"]
