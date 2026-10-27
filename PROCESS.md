## 1. TITULO FACHERO FACHERITO

En qué consiste el proyecto y que se busca resolver


Detalles de cómo instalar y visualizar el proyecto en el apartado **XX**.


## 2. Procedimiento

Los pasos para resolver este problema seguirán la siguiente metodología: 

1. Explorar los datos.
2. Hacer preguntas básicas de interés para el negocio.
3. Realizar EDA para responder las preguntas elegidas en el punto 2.
4. Hacer preguntas específicas asociadas a un tema de interés.
5. Buscar referencias para ampliar la visión sobre las preguntas específicas y las presentaciones de respuestas.


9.	Interpretar los resultados	Factores predictivos y análisis de errores.
10.	Comunicar conclusiones	Recomendaciones y limitaciones.


Categorías por tiendas
Cuales son las tiendas y que productos venden

## 2. Instalación

### 2.1. Clonar el proyecto desde github
Ve a www.github\bellodevdata\
Copia y pega en la terminal
```
git clone https:\\ XXXXX
```


### 2.2. Iniciar el proyecto
Para instalar el proyecto recomiendo tener el gestor de paquete uv instalado. Si no lo tienes puedes seguir las siguientes instrucciones para instalarlo:

UV es un gestor de paquete de Astral. Se puede instalar fácilmente usando:
```
pip install uv
```

En caso de algún problema con la instalación de UV puedes ver la documentación detallada de cómo instalarlo en:
<a href="https://docs.astral.sh/uv/getting-started/installation"/>https://docs.astral.sh/uv/getting-started/installation</a>

### 2.3. Crear ambiente virtual e instalar paqueterías
Gracias al gestor de paquetes UV basta con utilizar el siguiente comando en la terminal para crear el ambiente virtual e instalar las paqueterías:

```
uv sync
```

Para revisar con detalle las librerías o paqutería instalada revisa las secciones _requires-python_ y _dependencies_ en archivo **pyproject.toml**

Acá muestro un ejemplo de esas secciones sacadas del archivo pyproject.toml

``` 
requires-python = ">=3.13"
dependencies = [
    "matplotlib>=3.11.2",
    "numpy>=2.5.4",
    "pandas>=3.1.0",
    "scikit-learn>=1.9.1",
    "seaborn>=0.13.2",
]
```

### 1.4. Troubleshooting:

En caso de que no desees instalar UV y desees usar conda, pip u otro gestor de paquetes puedes instalar las paqueterías que se listan a continuación (Nota: Recuerda crear un ambiente virtual con una version de pytho 3.13 o superior):

Para crear un ambiente virtual usando pip
```
pip -m venv .venv --python
```

Las paqueterías las agregas utilizando
```
pip install numpy pandas scikit-learn matplotlib seaborn
```

<br>
<br>

