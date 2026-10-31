import streamlit as st
import pandas as pd

def apply_filters(df, filters):
    """ 
    Apply the selected filters to the DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing store data.
    filters (dict): A dictionary containing the selected filter values.

    Returns:
    pd.DataFrame: A DataFrame containing the filtered data.
    """    

    df_filtered = pd.DataFrame()
    df_filtered = df[
        df["region"].isin(filters["region"])
        & df["category"].isin(filters["category"])
        & df["socioeconomic_level"].isin(filters["socioeconomic_level"])
    ]
    
    if df_filtered.empty:
        st.warning("No hay datos para los filtros seleccionados.")
    
    return df_filtered