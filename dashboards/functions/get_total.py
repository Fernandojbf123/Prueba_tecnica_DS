import pandas as pd
import streamlit as st
from functions.warning_no_data import check_dataframe_empty

def get_top_stores_total(data: pd.DataFrame, top_n: int = 1) -> dict:
    """ 
    Get the top stores by total amount.

    Args:
        data (pd.DataFrame): The input data containing store transactions.

    Returns:
        dict: A dictionary containing the top store IDs and their corresponding total amounts.
        output_dict = {
            "store_ids": list,
            "top_amount_total": pd.DataFrame,
            "top_amount_card": pd.DataFrame,
            "top_amount_cash": pd.DataFrame,
            "top_units_sold": pd.DataFrame
        }
    """

    output_dict = {
        "store_id": [],
        "top_amount_total": pd.DataFrame(),
        "top_amount_card": pd.DataFrame(),
        "top_amount_cash": pd.DataFrame(),
        "top_units_sold": pd.DataFrame()
    }

    if check_dataframe_empty(data):
        return output_dict
    
    top_amount_total = data.groupby(["store_id","category"])["amount_total"].sum().sort_values(ascending=False).reset_index().head(top_n)

    if check_dataframe_empty(top_amount_total):
        return output_dict
    
    store_id = top_amount_total["store_id"].unique()
    top_amount_card = data[data["store_id"].isin(store_id)].groupby(["store_id","category"])["amount_card"].sum().sort_values(ascending=False).reset_index().head(top_n)
    top_amount_cash = data[data["store_id"].isin(store_id)].groupby(["store_id","category"])["amount_cash"].sum().sort_values(ascending=False).reset_index().head(top_n)
    top_units_sold = data[data["store_id"].isin(store_id)].groupby(["store_id","category"])["units_sold"].sum().sort_values(ascending=False).reset_index().head(top_n)

    output_dict = {
        "store_id": store_id.tolist(),
        "top_amount_total": top_amount_total,
        "top_amount_card": top_amount_card,
        "top_amount_cash": top_amount_cash,
        "top_units_sold": top_units_sold
    }

    return output_dict
