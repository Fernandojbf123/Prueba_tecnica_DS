import pandas as pd

def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Rellena los valores faltantes de las columnas amount_cash y cash_transactions

    Args:
        df (pd.DataFrame): El DataFrame con posibles valores faltantes.

    Returns:
        pd.DataFrame: El DataFrame con los valores faltantes rellenados.
    """

    df_amount_cash = df["amount_total"] - df["amount_card"]
    df_cash_transactions = df["total_transactions"] - df["card_transactions"]

    print(f"Cantidad de NaNs en amount_cash: {df['amount_cash'].isna().sum()}")
    print(f"Cantidad de NaNs en cash_transactions: {df['cash_transactions'].isna().sum()}")

    df["amount_cash"].fillna(df_amount_cash, inplace=True)
    df["cash_transactions"].fillna(df_cash_transactions, inplace=True)

    return df