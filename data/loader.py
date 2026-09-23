from pathlib import Path
import pandas as pd


DATA_DIR = Path(__file__).resolve().parent


def load_dataset() -> pd.DataFrame:
    csv_path = DATA_DIR / "global_superstore.csv"
    xlsx_path = DATA_DIR / "Sales_Dataset_2024.xlsx"

    if csv_path.exists():
        return pd.read_csv(csv_path, encoding="latin1")

    if xlsx_path.exists():
        return pd.read_excel(xlsx_path)

    raise FileNotFoundError(
        "Dataset not found in the data folder."
    )
