import matplotlib.pyplot as plt

def graficar_pred_vs_real(y_test: list, y_pred: list, final_de_titulo:str) -> None:
    """ 
    Grafica las predicciones del modelo frente a los valores reales.

    Parámetros:
    y_test : array-like
        Valores reales de las unidades vendidas.
    y_pred : array-like
        Valores predichos por el modelo.
    final_de_titulo : str
        Texto que se añadirá al final del título de la gráfica.
    """
    fig, ax = plt.subplots()
    ax.scatter(y_test, y_pred, label="Predicted vs Actual")
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], lw=2, color="red", linestyle="--", label="Ideal Fit")
    ax.legend()
    ax.set_xlabel("Actual Units Sold")
    ax.set_ylabel("Predicted Units Sold")
    ax.set_title(f"Actual vs Predicted Units Sold {final_de_titulo}")
    plt.show()