import streamlit as st
import pandas as pd

def render_sidebar_filters(df: pd.DataFrame) -> dict:
    """Sidebar with the dashboard filters. Returns the selected values."""
    st.sidebar.header("Filtros")
    regions = sorted(df["region"].dropna().unique())
    categories = sorted(df["category"].dropna().unique())
    levels = sorted(df["socioeconomic_level"].dropna().unique())

    return {
        "region": st.sidebar.multiselect("Región", regions, default=regions),
        "top_n": st.sidebar.selectbox("Top tiendas", [1, 3, 5, 10], index=1),
        "category": st.sidebar.multiselect("Categoría", categories, default=categories),
        "socioeconomic_level": st.sidebar.multiselect("Nivel socioeconómico", levels, default=levels),
    }