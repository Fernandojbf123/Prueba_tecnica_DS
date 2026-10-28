import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """ 
    Construye un preprocesador de datos para columnas categóricas y numéricas.
    Las columnas categóricas se imputan con la moda y se codifican con OneHotEncoder.
    Las columnas numéricas se imputan con la mediana y se escalan con StandardScaler.
    """

    categorical_features = [
        "store_id",
        "category",
        "store_format",
        "region",
        "socioeconomic_level",
    ]

    numeric_features = (
        X.select_dtypes(include=["number", "bool"])
        .columns
        .difference(categorical_features)
        .tolist()
    )

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    preprocessor = ColumnTransformer([
        ("categorical", categorical_pipeline, categorical_features),
        ("numeric", numeric_pipeline, numeric_features),
    ])

    return preprocessor