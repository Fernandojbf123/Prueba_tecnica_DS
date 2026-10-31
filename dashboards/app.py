import argparse
import os

import pandas as pd
import streamlit as st


from functions.load_data import load_csv
from functions.side_bar import render_sidebar_filters

from functions.apply_filters import apply_filters
from functions.get_total import get_top_stores_total


from functions.monthly_operations import (
    get_sums_by_selected_column,
    get_sums_by_category_and_column_for_store,
)   

from functions.graphics import (
    bar_plot_by_store,
    bar_plot_by_category
)

# Errorhandler
from functions.warning_no_data import check_dataframe_empty

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--version", type=str, default="20261028")
args, _ = arg_parser.parse_known_args()


@st.cache_data
def load_data(data_version: str) -> pd.DataFrame:
    data_dir = os.path.join(ROOT, "datasets", "raw", data_version)
    transactions = load_csv(os.path.join(data_dir, "transactions.csv"))
    stores = load_csv(os.path.join(data_dir, "stores.csv"))
    df = transactions.merge(stores, on="store_id", how="left")
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    
    return df


def main(version: str):
    st.set_page_config(page_title="Transactions Dashboard", layout="wide")
    st.title("Transactions Dashboard")

    # Load and filter data based on sidebar selections
    df = load_data(version)

    # Render sidebar filters and get selected values
    filters = render_sidebar_filters(df)

    # Apply filters to the dataframe based on selected sidebar values
    df_filtered =apply_filters(df, filters)


    st.text(f"Las {filters['top_n']} tiendas se eligen por la suma del monto total de las categorías elegidas")

    top_stores_total = get_top_stores_total(df_filtered, top_n = filters["top_n"])


    if not top_stores_total["store_id"]:
        st.warning("Debes seleccionar al menos una opción para Región, Categoría y Nivel socioeconómico")
        return 

    st.subheader("Totales")
    
    # Dividir en 2 columnas
    col1, col2 = st.columns(2)

    with col1:
        # colocar totales en forma de gráfico de barras
        df_top_amount_total = get_sums_by_selected_column(
            df = df_filtered, 
            store_id = top_stores_total["store_id"],
            col = "amount_total"
        )

        bar_plot_by_store(
            data = df_top_amount_total,
            y = "amount_total",
            title = "Total Amount by Store",
            x = "tspan",
            store_col = "store_id",
        )
    
    with col2:
        # colocar amount_other en forma de gráfico
        df_top_units_sold = get_sums_by_selected_column(
            df = df_filtered, 
            store_id = top_stores_total["store_id"],
            col = "units_sold"
        )
        bar_plot_by_store(
            data = df_top_units_sold,
            y = "units_sold",
            title = "Units Sold by Store",
            x = "tspan",
            store_col = "store_id",
        )


    st.subheader("Comparativas de ventas por:")
    col3, col4 = st.columns(2)
    # Elija una tienda
    selected_store_id = st.selectbox(
        "Selecciona una tienda",
        options=top_stores_total["store_id"]
    )
    
    with col3:
        df_sum = get_sums_by_category_and_column_for_store(
            df = df_filtered,
            store_id = selected_store_id,
            col = "amount_total"
        )

        bar_plot_by_category(
            data = df_sum,
            y = "amount_total",
            title = f"Total amount por cateogoría de la tienda {selected_store_id}",
            x = "tspan",
            category_col = "category",
        )

    with col4:
        df_sum = get_sums_by_category_and_column_for_store(
            df = df_filtered,
            store_id = selected_store_id,
            col = "units_sold"
        )

        bar_plot_by_category(
            data = df_sum,
            y = "units_sold",
            title = f"Total units sold por cateogoría de la tienda {selected_store_id}",
            x = "tspan",
            category_col = "category",
        )
    


if __name__ == "__main__":
    main(args.version)