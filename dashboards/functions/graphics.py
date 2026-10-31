import altair as alt
import pandas as pd
import streamlit as st

MONTH_AXIS = alt.Axis(format="%Y-%m", title="Mes")
STORE_COLORS = [
    "#1f77b4",
    "#d62728",
    "#2ca02c",
    "#9467bd",
    "#ff7f0e",
    "#17becf",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
]
CATEGORY_LINE_STYLES = {
    "Abarrotes": [1, 0],
    "Bebidas": [8, 4],
    "Cuidado_Personal": [3, 3],
    "Electronica": [12, 2],
    "Hogar": [12, 4],
    "Ropa": [5, 2],
}
CATEGORY_SYMBOLS = {
    "Abarrotes": "o",
    "Bebidas": "+",
    "Cuidado_Personal": "^",
    "Electronica": "s",
    "Hogar": "D",
    "Ropa": "x",
}



## Graficos
# Tipo 1: Bar plot
def bar_plot(data: pd.DataFrame, x: str, y: str, title: str):
    st.write(title)
    st.bar_chart(data = data, x=x, y= y)


# Tipo 2: Bar plot agrupado, un color por store_id
def bar_plot_by_store(
    data: pd.DataFrame,
    y: str,
    title: str,
    x: str = "tspan",
    store_col: str = "store_id",
):

    if data["store_id"].empty:
        return

    st.write(title)
    stores = sorted(data[store_col].unique())
    colors = [STORE_COLORS[i % len(STORE_COLORS)] for i in range(len(stores))]
    chart = (
        alt.Chart(data.sort_values(x))
        .mark_bar()
        .encode(
            x=alt.X(
                f"yearmonth({x}):O",
                axis=alt.Axis(format="%Y-%m", title="Mes", labelAngle=-45),
            ),
            y=alt.Y(f"{y}:Q", title=y),
            xOffset=alt.XOffset(f"{store_col}:N"),
            color=alt.Color(
                f"{store_col}:N",
                title="Tienda",
                scale=alt.Scale(domain=stores, range=colors),
                legend=alt.Legend(),
            ),
            tooltip=[
                alt.Tooltip(f"{store_col}:N", title="Tienda"),
                alt.Tooltip(f"{x}:T", format="%Y-%m", title="Mes"),
                alt.Tooltip(f"{y}:Q", format=",.0f"),
            ],
        )
        .properties(height=400)
    )
    st.altair_chart(chart, use_container_width=True)


# Tipo 3: Bar plot agrupado por mes, un color por categoría
def bar_plot_by_category(
    data: pd.DataFrame,
    y: str,
    title: str,
    x: str = "tspan",
    category_col: str = "category",
):
    if data.empty:
        return

    st.write(title)
    categories = sorted(data[category_col].unique())
    colors = [STORE_COLORS[i % len(STORE_COLORS)] for i in range(len(categories))]
    chart = (
        alt.Chart(data.sort_values(x))
        .mark_bar()
        .encode(
            x=alt.X(
                f"yearmonth({x}):O",
                axis=alt.Axis(format="%Y-%m", title="Mes", labelAngle=-45),
            ),
            y=alt.Y(f"{y}:Q", title=y),
            xOffset=alt.XOffset(f"{category_col}:N"),
            color=alt.Color(
                f"{category_col}:N",
                title="Categoría",
                scale=alt.Scale(domain=categories, range=colors),
                legend=alt.Legend(),
            ),
            tooltip=[
                alt.Tooltip(f"{category_col}:N", title="Categoría"),
                alt.Tooltip(f"{x}:T", format="%Y-%m", title="Mes"),
                alt.Tooltip(f"{y}:Q", format=",.0f"),
            ],
        )
        .properties(height=400)
    )
    st.altair_chart(chart, use_container_width=True)

