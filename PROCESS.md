## 1. PRUEBA TÉCNICA PARA DS

**Índice**

- [1. Prueba técnica para DS](#1-prueba-técnica-para-ds)
  - [1.1. Descripción del proyecto](#11-descripción-del-proyecto)
  - [1.2. Objetivo general](#12-objetivo-general)
  - [1.3. Objetivos específicos](#13-objetivos-específicos)
  - [1.4. Estructura del proyecto](#14-estructura-del-proyecto)
  - [1.5. Orden de ejecución](#15-orden-de-ejecución)
  - [1.6. Control de versiones de los datos](#16-control-de-versiones-de-los-datos)
- [2. Procedimiento](#2-procedimiento)
- [3. Resultados de cada paso](#3-resultados-de-cada-paso)
- [4. Conclusiones](#4-conclusiones)
- [5. Herramientas utilizadas](#5-herramientas-utilizadas)
- [6. Instalación](#6-instalación)
  - [6.1. Requisitos](#61-requisitos)
  - [6.2. Paqueterías utilizadas](#62-paqueterías-utilizadas)
  - [6.3. Clonar el proyecto desde GitHub](#63-clonar-el-proyecto-desde-github)
  - [6.4. Opción A (recomendada): instalar con uv](#64-opción-a-recomendada-instalar-con-uv)
  - [6.5. Opción B: instalar con pip](#65-opción-b-instalar-con-pip)
  - [6.6. Ejecutar el proyecto](#66-ejecutar-el-proyecto)
  - [6.7. Troubleshooting](#67-troubleshooting)

### 1.1. Descripción del proyecto

Proyecto de ciencia de datos para una cadena de retail con presencia en múltiples regiones de México. A partir del histórico diario de transacciones por tienda y categoría de producto (2023-01-01 a 2024-02-29), de las características de cada tienda y de un calendario de eventos, el proyecto:

1. Explora y limpia los datos (notebook `EDA.ipynb`).
2. Cuantifica y caracteriza los picos de ventas, y comprueba estadísticamente que se concentran en noviembre y diciembre.
3. Construye variables históricas (lags y medias móviles), entrena modelos de machine learning para predecir la demanda (`units_sold`) y los evalúa (notebook `processing_and_ML.ipynb`).

### 1.2. Objetivo general

Construir una solución basada en datos que apoye a operaciones a anticipar la demanda de la cadena, entendiendo cómo se comporta la actividad comercial y cuándo ocurren los picos de ventas.

### 1.3. Objetivos específicos

- Explorar los datasets `calendar`, `stores` y `transactions`, corregir tipos de datos y tratar los valores ausentes.
- Describir cómo se distribuye la actividad comercial entre tiendas y categorías.
- Cuantificar los picos de ventas (por encima del percentil 95 de cada tienda y categoría) e identificar cuándo y dónde ocurren.
- Contrastar estadísticamente (prueba Xi²) la hipótesis de que los picos se concentran en noviembre y diciembre.
- Preparar un dataset procesado con variables históricas (lags y medias móviles) sin fuga de información.
- Entrenar y comparar un modelo base, un modelo lineal y un modelo LightGBM para predecir `units_sold` por tienda y categoría.
- Evaluar los modelos con partición temporal (y, solo como comparativa, con partición aleatoria) y documentar conclusiones y limitaciones.

### 1.4. Estructura del proyecto

```
Prueba_Tecnica_DS/
├── datasets/
│   ├── raw/                 # Datos crudos, una subcarpeta por versión (AAAAMMDD)
│   │   └── 20261028/        # calendar.csv, stores.csv, transactions.csv
│   └── processed/           # Datos procesados (.pkl) listos para entrenar, un archivo por ejecución (AAAAMMDDHH_processed_data.pkl)
├── notebooks/
│   ├── EDA.ipynb                  # 1) Exploración, limpieza y análisis de picos de ventas
│   └── processing_and_ML.ipynb    # 2) Procesamiento, ingeniería de variables, entrenamiento y evaluación
├── functions/               # Funciones auxiliares reutilizables (p. ej. graficar_pred_vs_real.py)
├── pipelines/               # Pipelines de preprocesamiento de scikit-learn (preprocessing.py: build_preprocessor)
├── modelos/                 # Modelos entrenados (.joblib) generados al ejecutar processing_and_ML.ipynb
├── data_dictionary.md       # Diccionario de datos
├── PROCESS.md               # Este documento
├── README.md                # Enunciado de la prueba técnica
├── pyproject.toml           # Dependencias y versión de Python
└── uv.lock                  # Versiones exactas de las dependencias
```

### 1.5. Orden de ejecución

Los notebooks deben ejecutarse en este orden:

1. **`notebooks/EDA.ipynb`**: exploración inicial, limpieza y análisis de picos de ventas.
2. **`notebooks/processing_and_ML.ipynb`**: genera el dataset procesado, entrena los modelos y guarda los resultados en `datasets/processed/` y `modelos/`.

### 1.6. Control de versiones de los datos

- **Datos crudos**: cada versión se guarda en `datasets/raw/AAAAMMDD/` (fecha de la versión). Los notebooks seleccionan la versión con la variable `data_version`. Estos archivos sí están incluidos en el repositorio.
- **Datos procesados**: cada ejecución genera un archivo `datasets/processed/AAAAMMDDHH_processed_data.pkl` (fecha y hora de creación), que guarda `X`, `y` y metadatos.
- **Modelos entrenados**: se guardan en `modelos/` como `<nombre>_model.joblib`.
- Los archivos `.pkl` y `.joblib` **no se rastrean en el repositorio** (están en `.gitignore`) para mantenerlo ligero; se regeneran ejecutando los notebooks. El código se versiona con git y GitHub.


## 2. Procedimiento

Para resolver este problema se siguió la siguiente lógica de pensamiento:

1. Exploración inicial y ajustes de datos (convertir tipos y pasar fechas a formato `datetime`; sin hacer merge ni ingeniería de datos).
2. Hacer al menos 1 pregunta básica para describir el negocio, que sirva de base para llegar a una pregunta específica que aporte valor al negocio; en particular, información que le sirva a operaciones.
3. Entrenar modelos de ML para resolver la pregunta específica.
4. Conclusiones.

Cada paso incluye un pequeño análisis de los resultados obtenidos que sustenta o justifica el siguiente paso.


## 3. Resultados de cada paso
1. Exploración inicial  ajuste de datos.

**Dataset Calendar**
- Es un calendario de fechas.
- En líneas generales las columnas y sus datos estaban correctos
- Mejora principal, tipos de datos; algunas variables estaban en formato int64; lo cual podría generar mayor consumo de memoria, en este caso particular no hay problema porque la cantidad de datos del dataset es bastante pequeña.
- Solamente la columna "holiday_name" presentó valores ausentes o nulos, pero estos corresponden a días que no son festivos; por lo que se decidió dejarlos sin darle tratamiento.
- Las columnas "is_payday", "is_weekend", "is_navidad_season", "is_buen_fin", "is_semana_santa" son un complemento a la variable "holiday_name"; también se quedaron sin tratamiento.

**Dataset Stores**
- Este dataset aporta información sobre las tiendas; como su formato, en qué región está ubicada, cantidad de cajas.
- No contiene datos nulos o ausentes
- En general no se detectaron anomalías en los valores.
- El mínimo de cajas son 4 y el máximo 37
- Los metros cuadrados de las tiendas van entre 737 a 14784 sqm (metros cuadrados); y por este motivo, se decidió hacer un histograma para ver la distribución de tamaños de las tiendas
- El dataset contiene tiendas que fueron abiertas entre 2010 y 2022.
- Dicho todo lo anterior, se puede decir que este dataset aporta buenas ideas para algunas preguntas significativas las cuales exploraremos al final de esta sección.

**Dataset Transactions**
- Este dataset ofrece los consolidados diarios de cada una de las tiendas por categorías.
- La documentación dice que es posible que hayan datos ausentes al final del periodo; por este motivo se exploró con más detenimiento los datos ausentes con el objetivo de ver relaciones, si hay agrupamiento o patrones.
- La columna cash_transactions; para agregar los datos faltantes se decidió hacer una función que haga la resta entre total_transactions y card_transactions.
- La columna amount_cash también tiene datos ausentes; por lo que se deciden completar los datos haciendo la restra entre amount_total con amound_card;
- La columna units sold también tiene datos ausentes; las fechas en que faltan los datos
- La columna avg_ticket también tiene valores ausentes; y tambien se decide rellenar estos valores con el valor del ticket promedio para la tienda.
- La columna replenish_signal también tiene valores ausentes; y dada la información de data_dictionary.md se decidió revisar en qué fechas estaban los ausentes; encontrando que los ausentes solo se encontraban en 2023-01-01 y 2023-01-02. Específicamente, el valor ausente ocurre en las 6 categorías de las 80 tiendas. Es probable que los valores que falten se deban a la inicialización del sistema durante la extracción de datos. Se dejarán como ausentes ya que desconoce la forma en que son calculados y además porque evidentemente dependen del histórico.

**2. Pregunta básica de interés para el negocio**

- ¿Cómo se distribuye la actividad comercial del negocio entre las tiendas y categorías, y qué diferencias relevantes existen en sus niveles de ventas y volumen de transacciones?

Justificación: Permite identificar cómo está compuesto el negocio; así como establecer referencias descriptivas y sentar las bases para hacer estudios de estadística inferencial.

Principales hallazgos:

- Diferencias entre tiendas: STR_017 presenta un nivel de ventas generalmente superior al de las demás tiendas analizadas, tanto en su media como en su mediana.
- Dispersión y valores extremos: las distribuciones muestran una cola superior más larga que la cola inferior, así como presencia de outliers. Esto evidencia heterogeneidad en los importes de venta y motiva investigar los factores asociados a los incrementos observados.
- Se justifica la investigación de los valores elevados y si estos corrpesponden a promociones, festivos o si son propios de la dinámica de ventas del negocio.

Dicho lo anterior; para realizar la investigación se desarrolló el siguiente plan de trabajo:

Fase 1. Cuantificar los picos de ventas
Fase 2. Investigar cuándo y dónde ocurren los picos
Fase 3. Establecer un problema a resolver con ML.
Fase 4. Preparar los datos para entrenar un modelo
Fase 5. Entrenar y evaluar modelos (regresión lineal como dummy y LightGBM)
Fase 6. Traducir predicciones en decisiones operativas


## 4. Conclusiones

- El modelo base obtiene el mejor resultado en test temporal. Presenta un R² de 0.66 y un MSE de aproximadamente 580,000, frente a 0.61 y 1,020,000 del modelo lineal, y 0.65 y 899,000 de LightGBM. En esta evaluación, los modelos más complejos no muestran una mejora clara respecto al modelo base.

- El rendimiento disminuye al evaluar periodos posteriores. El R² del modelo lineal baja de 0.77 en entrenamiento a 0.61 en test, mientras que LightGBM pasa de 0.87 a 0.65. Este deterioro podría estar relacionado con cambios en la distribución de la demanda entre ambos periodos. El análisis exploratorio identificó una mayor concentración de ventas en noviembre y diciembre, por lo que conviene comprobar si estos meses están representados en el conjunto de prueba y cómo afectan al error.

- LightGBM mejora moderadamente al modelo lineal en test temporal. Su MSE disminuye aproximadamente un 12 % y su R² aumenta cuatro puntos porcentuales. Aunque LightGBM presenta un mejor ajuste en entrenamiento, la diferencia de rendimiento en test es más limitada, por lo que no puede concluirse que su mayor complejidad aporte una ventaja sustancial.

- La partición aleatoria produce métricas más favorables, pero no representa adecuadamente la predicción futura. LightGBM obtiene un R² de 0.84 y un MSE de aproximadamente 246,000 con esta estrategia, frente a 0.65 y 899,000 con la partición temporal. La diferencia evidencia la importancia de respetar el orden cronológico al evaluar modelos de pronóstico. Las métricas aleatorias no deben utilizarse como estimación principal del rendimiento futuro.

- La diferencia entre entrenamiento y test requiere un análisis adicional. La brecha de rendimiento observada en LightGBM puede reflejar tanto sobreajuste como cambios temporales en la demanda. Con los resultados disponibles no es posible determinar qué proporción corresponde a cada factor.

**Limitaciones y trabajo futuro:**

- Implementar validación temporal mediante TimeSeriesSplit u otra estrategia de origen móvil (rolling-origin validation) para comprobar la estabilidad del rendimiento entre distintos periodos.

- Definir una evaluación que reproduzca el horizonte de predicción de siete días y garantice que las variables utilizadas estén disponibles en el momento de generar el pronóstico.

- Analizar el error por mes, tienda y categoría, prestando especial atención a los periodos de demanda elevada, como noviembre y diciembre.

- Comparar los modelos con un pronóstico de referencia (baseline), por ejemplo, utilizar las ventas del mismo día de la semana anterior.

- Evaluar métricas adicionales, como MAE y WAPE, para complementar el MSE y facilitar la interpretación del error en unidades vendidas.


## 5. Herramientas utilizadas

- **Entorno de desarrollo**: Visual Studio Code.
- **Gestión de entorno y paquetes**: uv.
- **Librerías**: pandas, numpy, scipy, scikit-learn, LightGBM, matplotlib y seaborn.
- **Documentación y referencias**: documentación de scikit-learn, búsquedas en Google y ejemplos de kaggle.com.
- **Herramientas de IA**: OpenCode, ChatGPT (modelos Luna y Terra), Claude Sonnet 5.5 y GitHub Copilot.
- **Control de versiones**: git y GitHub.


## 6. Instalación

### 6.1. Requisitos

- Python 3.13 o superior (ver `requires-python` en `pyproject.toml`).
- git.
- Un entorno que ejecute notebooks de Jupyter (por ejemplo, VSCode con las extensiones de Python y Jupyter).

### 6.2. Paqueterías utilizadas

| Paquete | Versión mínima | Uso |
|---------|----------------|-----|
| pandas | 3.1.0 | Manipulación de datos |
| numpy | 2.5.4 | Cálculo numérico |
| scipy | 1.18.1 | Prueba Xi² (`chi2_contingency`) |
| scikit-learn | 1.9.1 | Preprocesamiento, modelo lineal, métricas y pipelines (instala también `joblib`) |
| lightgbm | 4.7.0 | Modelo LightGBM |
| matplotlib | 3.11.2 | Gráficas |
| seaborn | 0.13.2 | Gráficas estadísticas |
| ipykernel | – | Ejecutar los notebooks (no está en `pyproject.toml`; VSCode ofrece instalarlo al elegir el kernel) |

### 6.3. Clonar el proyecto desde GitHub

```
git clone https://github.com/Fernandojbf123/Prueba_tecnica_DS.git
cd Prueba_tecnica_DS
```

### 6.4. Opción A (recomendada): instalar con uv

uv es un gestor de paquetes de Astral. Para instalarlo:

```
pip install uv
```

Si tienes problemas, consulta la documentación oficial: [https://docs.astral.sh/uv/getting-started/installation](https://docs.astral.sh/uv/getting-started/installation)

Después, desde la raíz del proyecto, crea el ambiente virtual e instala las paqueterías exactas de `uv.lock`:

```
uv sync
```

Esto crea la carpeta `.venv`. Selecciona ese entorno como kernel al abrir los notebooks.

### 6.5. Opción B: instalar con pip

Desde la raíz del proyecto, con Python 3.13 o superior:

1. Crear el ambiente virtual:

   ```
   python3.13 -m venv .venv
   ```

2. Activarlo:

   ```
   # Linux / macOS
   source .venv/bin/activate

   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   ```

3. Instalar las paqueterías:

   ```
   pip install pandas numpy scipy scikit-learn lightgbm matplotlib seaborn ipykernel
   ```

### 6.6. Ejecutar el proyecto

1. Abre `notebooks/EDA.ipynb` y ejecútalo completo.
2. Abre `notebooks/processing_and_ML.ipynb` y ejecútalo completo. Generará los archivos en `datasets/processed/` y `modelos/`.

Los notebooks usan rutas relativas (`..`), por lo que deben ejecutarse con la carpeta `notebooks/` como directorio de trabajo.

### 6.7. Troubleshooting

- Si usas conda u otro gestor, crea un ambiente con Python 3.13 o superior e instala las paqueterías de la tabla de la sección 6.2 con `pip`.
- Si aparece `ModuleNotFoundError` al importar `functions` o `pipelines`, verifica que ejecutas los notebooks desde la carpeta `notebooks/`.

