import pandas as pd
import streamlit as st

def get_sums_by_selected_column(df: pd.DataFrame, store_id: list, col: str) -> pd.DataFrame:
    """
    For the specified category, calculate the monthly sums for each store and return the top N stores.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing store data.
    store_id ([list]): The list of store IDs to include.
    col (str): The column name to use for calculating sums.

    Returns:
    pd.DataFrame: A DataFrame containing the top N stores based on monthly sums.
    """
    if df.empty:
        st.warning("No ha seleccionado ninguna opción")
        return pd.DataFrame()

    if not store_id:
        st.warning("No ha seleccionado ninguna tienda")
        return pd.DataFrame()

    if not col:
        st.warning("No ha seleccionado ninguna categoría")
        return pd.DataFrame()
                
    top_stores = df[df["store_id"].isin(store_id)].groupby(["store_id","year","month"])[col].sum().reset_index()
    top_stores = top_stores.sort_values(by=["year","month"], ascending=True)
    tspan = pd.to_datetime(top_stores["year"].astype(str) + "-" + top_stores["month"].astype(str), format="%Y-%m")
    top_stores["tspan"] = tspan
    
    return top_stores


def get_sums_by_category_and_column_for_store(df: pd.DataFrame, store_id: str, col: str) -> pd.DataFrame:
    if df.empty:
        st.warning("No ha seleccionado ninguna opción")
        return pd.DataFrame()

    if not store_id:
        st.warning("No ha seleccionado ninguna tienda")
        return pd.DataFrame()

    if not col:
        st.warning("No ha seleccionado ninguna columna")
        return pd.DataFrame()

    df_filtered = df[(df["store_id"] == store_id)].groupby(["category","year","month"])[col].sum().reset_index()
    df_filtered = df_filtered.sort_values(by=["year","month"], ascending=True)
    tspan = pd.to_datetime(df_filtered["year"].astype(str) + "-" + df_filtered["month"].astype(str), format="%Y-%m")
    df_filtered["tspan"] = tspan

    return df_filtered
