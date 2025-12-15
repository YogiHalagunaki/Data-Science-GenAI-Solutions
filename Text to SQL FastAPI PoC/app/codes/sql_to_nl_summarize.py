import pandas as pd
from utils import custom_logger as clogs

def dataframe_to_text(df: pd.DataFrame) -> str:
    if df.empty:
        return "No results found."

    # If single value (aggregation)
    if df.shape == (1, 1):
        col = df.columns[0]
        val = df.iloc[0, 0]
        return f"The {col} is {val}."

    # If small table
    if len(df) <= 5 and len(df.columns) <= 5:
        return "Here are the results: " + df.to_dict(orient="records").__str__()
    clogs.logging.info()
    # Otherwise, summarize
    return f"Returned {len(df)} rows and {len(df.columns)} columns. Showing first few rows: {df.head(3).to_dict(orient='records')}"
