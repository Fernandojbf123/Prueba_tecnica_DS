import pandas as pd


def show_totals(df: pd.DataFrame):
    """
    Display the total amount and total units sold for the given DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing store data.
    """
    for 
    total_amount = df["amount"].sum()
    total_units_sold = df["units_sold"].sum()
    st.write(f"Total Amount: {total_amount}")
    st.write(f"Total Units Sold: {total_units_sold}")