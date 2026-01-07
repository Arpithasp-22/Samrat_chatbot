import pandas as pd
import os

# Find project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "C:\\Users\\Arpitha.s\\Desktop\\Samrat_chatbot\\data\\All_combined_22-25.csv")

# Load CSV
df = pd.read_csv(CSV_PATH)

# Clean column names
df.columns = df.columns.str.strip()

# Ignore junk columns
if "Area" in df.columns:
    df = df.loc[:, :"Area"]

# Normalize columns
df["City"] = df["City"].astype(str).str.strip().str.lower()
df["Basic Amount"] = pd.to_numeric(df["Basic Amount"], errors="coerce").fillna(0)


def get_total_sales_by_city(city):
    city = city.lower().strip()
    return df[df["City"] == city]["Basic Amount"].sum()


# TEMP TEST — this is intentional
if __name__ == "__main__":
    print(get_total_sales_by_city("hyderabad"))
