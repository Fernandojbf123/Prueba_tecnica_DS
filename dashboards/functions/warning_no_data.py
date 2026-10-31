import streamlit as st

def check_dataframe_empty(df):
    if df.empty:
        st.warning("Elija al menos una opción de Región, Categoría y Nivel socioeconómico")
        return True
    return False
        