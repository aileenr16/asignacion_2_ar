# -*- coding: utf-8 -*-
"""asignacion2_ar.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FDS7rTtfCpl9YtTmpKAKRUUfAI77ihb7
"""

# This code is exactly the same as what we have done in the previous exercises. You do not need to read it again.
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import r2_score
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

df = pd.read_csv('/content/drive/My Drive/asignacion2/week3.csv')

print(df.head())
print(df.columns)

# Cambiar el nombre de la columna
df.reset_index(inplace=True)
df.columns = ['X1', 'X2', 'y_objetivo']
df.head()
df.shape

"""# Creación de Gráfico en 3D"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

X1 = df['X1']
X2 = df['X2']
y_objetivo = df['y_objetivo']


# Crear la figura y un objeto 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Crear gráfico de dispersión 3D
ax.scatter(X1, X2, y_objetivo, c='b', marker='o', alpha=0.6)

# Establecer etiquetas para cada eje
ax.set_xlabel('Característica 1 (X1)')
ax.set_ylabel('Característica 2 (X2)')
ax.set_zlabel('Valor Objetivo (y)')

# Título del gráfico
ax.set_title('Gráfico de dispersión 3D')

# Mostrar el gráfico
plt.show()

import plotly.graph_objs as go
import pandas as pd
import numpy as np



# Crear el gráfico 3D interactivo
fig = go.Figure(data=[go.Scatter3d(
    x=X1,
    y=X2,
    z=y_objetivo,
    mode='markers',
    marker=dict(
        size=5,
        color=y_objetivo,  # Color basado en el objetivo
        colorscale='Viridis',  # Escala de color
        opacity=0.8
    )
)])

# Configurar etiquetas y título
fig.update_layout(
    scene=dict(
        xaxis_title='Característica 1 (X1)',
        yaxis_title='Característica 2 (X2)',
        zaxis_title='Valor Objetivo (y)'
    ),
    title='Gráfico de dispersión 3D interactivo'
)

# Mostrar el gráfico
fig.show()

"""# Agregar caracteristicas polinomicas"""

from sklearn.preprocessing import PolynomialFeatures
# Crearemos la función para convertir y reemplazar una columna en el dataset original a una polinomica




def convert_to_polynomial(df, feature , degree, columna_obj):

    # Creamos el objeto PolynomialFeatures
    poly_features = PolynomialFeatures(degree=degree, include_bias=False)

    # Decidimos a que caracteristica le vamos a clonar o ha cambiar el tipo de datos y que transformación
    X_poly = poly_features.fit_transform(df[[feature]])

    # Guardaremos la columna agregada 'Polinomial' basada en el Feature que seleccionemos y guardaremos en un DataFrame Temporal
    df_poly_transformed = pd.DataFrame(X_poly, columns=[f'X_{feature}_{i}' for i in range(1, degree + 1)])

    # Eliminamos la primera columna
    df_poly_transformed = df_poly_transformed.drop(df_poly_transformed.columns[0], axis=1)

    # Reemplazaremos la última columna del dataframe emergente creado, en el dataframe de entrada a la función
    # Unir los dataframes
    df = pd.concat([df, df_poly_transformed], axis=1)

    # Mover la columna 'y_objetivo' al final
    df[columna_obj] = df.pop(columna_obj)


    #print(df.head())
    return df

# Probaremos la función en el dataset original

df = convert_to_polynomial(df,'X1', 5, 'y_objetivo')
df = convert_to_polynomial(df,'X2', 5, 'y_objetivo')

print(df.columns)
print(df.head())

"""# Entrenamiendo del Modelo De Regresión Lineal Multiple

Dividiremos los datos para el entrenamiento
"""

# Separaremos el dataset
X = df[['X1', 'X2', 'X_X1_2', 'X_X1_3', 'X_X1_4', 'X_X1_5', 'X_X2_2', 'X_X2_3',
       'X_X2_4', 'X_X2_5']]
y = df['y_objetivo']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""Vamos a implementar una función para entrenar modelos"""

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

def train_test_model(model, dataset, column_obj, perc_test=0.3):
    """
    Función para entrenar y evaluar un modelo de machine learning.

    Parámetros:
    - model: el modelo a entrenar (por ejemplo, LogisticRegression(), LinearRegression(), etc.)
    - dataset: el DataFrame con los datos de entrada.
    - column_obj: el nombre de la columna objetivo.
    - perc_test: porcentaje de datos para el conjunto de prueba (test), valor por defecto = 0.3.

    Retorna:
    - Un diccionario con el modelo entrenado, las predicciones, MSE, R2, coeficientes e intercepto.
    """

    # Seleccionar las características (X) y la columna objetivo (y)
    feature_columns = [col for col in dataset.columns if col != column_obj]
    X = dataset[feature_columns]
    y = dataset[column_obj]

    # Dividir el dataset en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=perc_test, random_state=42)

    # Entrenar el modelo
    trained_model = model.fit(X_train, y_train)

    # Predecir los valores de 'y' en el conjunto de prueba
    predictions = trained_model.predict(X_test)

    # Obtener coeficientes e intercepto (si el modelo los tiene)
    coef = getattr(trained_model, 'coef_', None)  # Retorna None si el modelo no tiene coef_
    intercept = getattr(trained_model, 'intercept_', None)  # Retorna None si no tiene intercepto

    # Calcular el error cuadrático medio (MSE) y el coeficiente de determinación (R2)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    # Imprimir los resultados
    print(f"Modelo entrenado: {trained_model}")
    print(f"Coeficientes del modelo: {coef}")
    print(f"Intercepto del modelo: {intercept}")
    print(f"\nError cuadrático medio (MSE): {mse:.4f}")
    print(f"Coeficiente de determinación (R2): {r2:.4f}")

    # Visualizar los resultados con un gráfico
    plt.scatter(y_test, predictions, color='blue')
    plt.xlabel('Valores Reales')
    plt.ylabel('Valores Predichos')
    plt.title('Real vs. Predicho')
    plt.show()

    # Retornar el modelo entrenado y otros resultados en un diccionario
    return {
        'trained_model': trained_model,
        'predictions': predictions,
        'mse': mse,
        'r2': r2,
        'coefficients': coef,
        'intercept': intercept
    }

"""Modelo Lasso entrenado para alpha 0.00001"""

# Ejemplo de uso:
trained_model_results_1 = train_test_model(Lasso(alpha=0.00001), df, 'y_objetivo', perc_test=0.2)
# Puedes acceder a los resultados:
trained_lasso_1 = trained_model_results_1['trained_model']

"""Modelo Lasso entrenado para alpha 0.0001"""

# Ejemplo de uso:
trained_model_results_2 = train_test_model(Lasso(alpha=0.0001), df, 'y_objetivo', perc_test=0.2)
# Puedes acceder a los resultados:
trained_lasso_2 = trained_model_results_2['trained_model']

"""Modelo Lasso entrenado para alpha 0.001"""

# Ejemplo de uso:
trained_model_results_3 = train_test_model(Lasso(alpha=0.001), df, 'y_objetivo', perc_test=0.2)
# Puedes acceder a los resultados:
trained_lasso_3 = trained_model_results_3['trained_model']

"""Modelo Lasso entrenado para alpha 0.01"""

# Ejemplo de uso:
trained_model_results_4 = train_test_model(Lasso(alpha=0.01), df, 'y_objetivo', perc_test=0.2)
# Puedes acceder a los resultados:
trained_lasso_4 = trained_model_results_4['trained_model']

"""Modelo Lasso entrenado para alpha 0.1"""

# Ejemplo de uso:
trained_model_results_5 = train_test_model(Lasso(alpha=0.1), df, 'y_objetivo', perc_test=0.2)
# Puedes acceder a los resultados:
trained_lasso_5 = trained_model_results_5['trained_model']

"""Modelo Lasso entrenado para alpha 1"""

# Ejemplo de uso:
trained_model_results_6 = train_test_model(Lasso(alpha=1), df, 'y_objetivo', perc_test=0.2)
# Puedes acceder a los resultados:
trained_lasso_6 = trained_model_results_6['trained_model']

"""# Cuadricula de Valores de Caracteristicas

Vamos a generar los valores de caracteristicas para columna, exceptuando la columna objetivo
"""

# Excluir la columna 'y_objetivo'
df_excluido = df.drop(columns=['y_objetivo'])

# Encontrar los valores máximos y mínimos de cada columna
valores_maximos = df_excluido.max()
valores_minimos = df_excluido.min()

# Mostrar los resultados
for columna in df_excluido.columns:
    print(f"Columna: {columna}")
    print(f"Valor máximo: {valores_maximos[columna]}")
    print(f"Valor mínimo: {valores_minimos[columna]}")
    print()

"""Vamos a generar un dataset con los valores de cuadriculas, basandose en los minimos y máximos encontrados en el bloque anterior"""

# Definir el rango y la cantidad de puntos para cada característica
num_samples = 100  # Número de muestras que deseas
num_features = 10
value_range = (-3, 3)

# Generar datos aleatorios en el rango especificado
data = np.random.uniform(value_range[0], value_range[1], size=(num_samples, num_features))

# Convertir a un DataFrame de pandas
df_cuadricula = pd.DataFrame(data, columns=[f'feature_{i+1}' for i in range(num_features)])

# Mostrar las primeras filas del DataFrame
print(df_cuadricula.head())

"""Vamos a probar un modelo ya entrenado, utilizando el df_cuadricula para revisar las respuestas predichas por el modelo"""

# Renombrar las columnas de df_cuadricula para que coincidan con las del modelo entrenado
df_cuadricula.columns = ['X1', 'X2', 'X_X1_2', 'X_X1_3', 'X_X1_4', 'X_X1_5', 'X_X2_2', 'X_X2_3', 'X_X2_4', 'X_X2_5']

# Realizar la predicción
predictions_1 = trained_lasso_1.predict(df_cuadricula)

# Mostrar las predicciones
print("Predicciones para los nuevos datos:")
print(predictions_1)

import plotly.graph_objs as go
import pandas as pd
import numpy as np


# Extraer la característica 'X2' del DataFrame
X1 = df_cuadricula['X2']

# Crear un vector de ceros del mismo tamaño que X1 para representar 'X2'
X2 = np.zeros(len(X1))  # Esto crea un array de ceros del mismo tamaño que X1

y_objetivo = predictions_1

# Crear el gráfico 3D interactivo
fig = go.Figure(data=[go.Scatter3d(
    x=X1,  # Característica 1 en el eje X
    y=X2,  # Característica 2 en el eje Y (valores constantes en 0)
    z=predictions_1,  # Predicciones en el eje Z
    mode='markers',
    marker=dict(
        size=5,
        color=predictions_1,  # Color basado en las predicciones
        colorscale='Viridis',  # Escala de color
        opacity=0.8
    )
)])

# Configurar etiquetas y título
fig.update_layout(
    scene=dict(
        xaxis_title='Característica 1 (X2)',
        yaxis_title='Característica 2 (Constante 0)',
        zaxis_title='Valor Objetivo (Predicción)'
    ),
    title='Gráfico de dispersión 3D interactivo'
)

# Mostrar el gráfico
fig.show()

# Realizar la predicción
predictions_2 = trained_lasso_2.predict(df_cuadricula)

# Mostrar las predicciones
print("Predicciones para los nuevos datos:")
print(predictions_2)

import plotly.graph_objs as go
import pandas as pd
import numpy as np


# Extraer la característica 'X2' del DataFrame
X1 = df_cuadricula['X2']

# Crear un vector de ceros del mismo tamaño que X1 para representar 'X2'
X2 = np.zeros(len(X1))  # Esto crea un array de ceros del mismo tamaño que X1

y_objetivo = predictions_2

# Crear el gráfico 3D interactivo
fig = go.Figure(data=[go.Scatter3d(
    x=X1,  # Característica 1 en el eje X
    y=X2,  # Característica 2 en el eje Y (valores constantes en 0)
    z=predictions_2,  # Predicciones en el eje Z
    mode='markers',
    marker=dict(
        size=5,
        color=predictions_2,  # Color basado en las predicciones
        colorscale='Viridis',  # Escala de color
        opacity=0.8
    )
)])

# Configurar etiquetas y título
fig.update_layout(
    scene=dict(
        xaxis_title='Característica 1 (X2)',
        yaxis_title='Característica 2 (Constante 0)',
        zaxis_title='Valor Objetivo (Predicción)'
    ),
    title='Gráfico de dispersión 3D interactivo'
)

# Mostrar el gráfico
fig.show()

# Realizar la predicción
predictions_3 = trained_lasso_3.predict(df_cuadricula)

# Mostrar las predicciones
print("Predicciones para los nuevos datos:")
print(predictions_3)

import plotly.graph_objs as go
import pandas as pd
import numpy as np



# Extraer la característica 'X2' del DataFrame
X1 = df_cuadricula['X2']

# Crear un vector de ceros del mismo tamaño que X1 para representar 'X2'
X2 = np.zeros(len(X1))  # Esto crea un array de ceros del mismo tamaño que X1

y_objetivo = predictions_3

# Crear el gráfico 3D interactivo
fig = go.Figure(data=[go.Scatter3d(
    x=X1,  # Característica 1 en el eje X
    y=X2,  # Característica 2 en el eje Y (valores constantes en 0)
    z=predictions_3,  # Predicciones en el eje Z
    mode='markers',
    marker=dict(
        size=5,
        color=predictions_3,  # Color basado en las predicciones
        colorscale='Viridis',  # Escala de color
        opacity=0.8
    )
)])

# Configurar etiquetas y título
fig.update_layout(
    scene=dict(
        xaxis_title='Característica 1 (X2)',
        yaxis_title='Característica 2 (Constante 0)',
        zaxis_title='Valor Objetivo (Predicción)'
    ),
    title='Gráfico de dispersión 3D interactivo'
)

# Mostrar el gráfico
fig.show()

# Realizar la predicción
predictions_4 = trained_lasso_4.predict(df_cuadricula)

# Mostrar las predicciones
print("Predicciones para los nuevos datos:")
print(predictions_4)

import plotly.graph_objs as go
import pandas as pd
import numpy as np


# Extraer la característica 'X2' del DataFrame
X1 = df_cuadricula['X2']

# Crear un vector de ceros del mismo tamaño que X1 para representar 'X2'
X2 = np.zeros(len(X1))  # Esto crea un array de ceros del mismo tamaño que X1

y_objetivo = predictions_4

# Crear el gráfico 3D interactivo
fig = go.Figure(data=[go.Scatter3d(
    x=X1,  # Característica 1 en el eje X
    y=X2,  # Característica 2 en el eje Y (valores constantes en 0)
    z=predictions_4,  # Predicciones en el eje Z
    mode='markers',
    marker=dict(
        size=5,
        color=predictions_4,  # Color basado en las predicciones
        colorscale='Viridis',  # Escala de color
        opacity=0.8
    )
)])

# Configurar etiquetas y título
fig.update_layout(
    scene=dict(
        xaxis_title='Característica 1 (X2)',
        yaxis_title='Característica 2 (Constante 0)',
        zaxis_title='Valor Objetivo (Predicción)'
    ),
    title='Gráfico de dispersión 3D interactivo'
)

# Mostrar el gráfico
fig.show()

# Realizar la predicción nuevamente
predictions_5 = trained_lasso_5.predict(df_cuadricula)

# Mostrar las predicciones
print("Predicciones para los nuevos datos:")
print(predictions_5)

import plotly.graph_objs as go
import pandas as pd
import numpy as np


# Extraer la característica 'X2' del DataFrame
X1 = df_cuadricula['X2']

# Crear un vector de ceros del mismo tamaño que X1 para representar 'X2'
X2 = np.zeros(len(X1))  # Esto crea un array de ceros del mismo tamaño que X1

# Asumimos que `predictions_5` es el resultado de las predicciones en el eje Z
y_objetivo = predictions_5

# Crear el gráfico 3D interactivo
fig = go.Figure(data=[go.Scatter3d(
    x=X1,  # Característica 1 en el eje X
    y=X2,  # Característica 2 en el eje Y (valores constantes en 0)
    z=predictions_5,  # Predicciones en el eje Z
    mode='markers',
    marker=dict(
        size=5,
        color=predictions_5,  # Color basado en las predicciones
        colorscale='Viridis',  # Escala de color
        opacity=0.8
    )
)])

# Configurar etiquetas y título
fig.update_layout(
    scene=dict(
        xaxis_title='Característica 1 (X2)',
        yaxis_title='Característica 2 (Constante 0)',
        zaxis_title='Valor Objetivo (Predicción)'
    ),
    title='Gráfico de dispersión 3D interactivo'
)

# Mostrar el gráfico
fig.show()

# Realizar la predicción
predictions_6 = trained_lasso_6.predict(df_cuadricula)

# Mostrar las predicciones
print("Predicciones para los nuevos datos:")
print(predictions_6)

import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Extraer la característica 'X2' del DataFrame
X1 = df_cuadricula['X2']

# Crear un vector de ceros del mismo tamaño que X1 para representar 'X2'
X2 = np.zeros(len(X1))  # Esto crea un array de ceros del mismo tamaño que X1

y_objetivo = predictions_6

# Crear el gráfico 3D interactivo
fig = go.Figure(data=[go.Scatter3d(
    x=X1,  # Característica 1 en el eje X
    y=X2,  # Característica 2 en el eje Y (valores constantes en 0)
    z=predictions_6,  # Predicciones en el eje Z
    mode='markers',
    marker=dict(
        size=5,
        color=predictions_6,  # Color basado en las predicciones
        colorscale='Viridis',  # Escala de color
        opacity=0.8
    )
)])

# Configurar etiquetas y título
fig.update_layout(
    scene=dict(
        xaxis_title='Característica 1 (X2)',
        yaxis_title='Característica 2 (Constante 0)',
        zaxis_title='Valor Objetivo (Predicción)'
    ),
    title='Gráfico de dispersión 3D interactivo'
)

# Mostrar el gráfico
fig.show()

"""# Regresión de Ridge"""

from sklearn.linear_model import Ridge

# Ejemplo de uso:
trained_ridge_results_1 = train_test_model(Ridge(alpha=0.00001), df, 'y_objetivo', perc_test=0.2)

# Puedes acceder a los resultados:
trained_ridge_1 = trained_ridge_results_1['trained_model']

from sklearn.linear_model import Ridge

# Ejemplo de uso:
trained_ridge_results_2 = train_test_model(Ridge(alpha=0.0001), df, 'y_objetivo', perc_test=0.2)

# Puedes acceder a los resultados:
trained_ridge_2 = trained_ridge_results_2['trained_model']

from sklearn.linear_model import Ridge

# Ejemplo de uso:
trained_ridge_results_3 = train_test_model(Ridge(alpha=0.001), df, 'y_objetivo', perc_test=0.2)

# Puedes acceder a los resultados:
trained_ridge_3 = trained_ridge_results_3['trained_model']

from sklearn.linear_model import Ridge

# Ejemplo de uso:
trained_ridge_results_4 = train_test_model(Ridge(alpha=0.01), df, 'y_objetivo', perc_test=0.2)

# Puedes acceder a los resultados:
trained_ridge_4 = trained_ridge_results_4['trained_model']

from sklearn.linear_model import Ridge

# Ejemplo de uso:
trained_ridge_results_5 = train_test_model(Ridge(alpha=0.1), df, 'y_objetivo', perc_test=0.2)

# Puedes acceder a los resultados:
trained_ridge_5 = trained_ridge_results_5['trained_model']

from sklearn.linear_model import Ridge

# Ejemplo de uso:
trained_ridge_results_6 = train_test_model(Ridge(alpha=1), df, 'y_objetivo', perc_test=0.2)

# Puedes acceder a los resultados:
trained_ridge_6 = trained_ridge_results_6['trained_model']

# Realizar la predicción
predictions_ridge_1 = trained_ridge_1.predict(df_cuadricula)

# Mostrar las predicciones
print("Predicciones para los nuevos datos:")
print(predictions_ridge_1)

import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Extraer la característica 'X2' del DataFrame
X1 = df_cuadricula['X2']

# Crear un vector de ceros del mismo tamaño que X1 para representar 'X2'
X2 = np.zeros(len(X1))  # Esto crea un array de ceros del mismo tamaño que X1

y_objetivo = predictions_ridge_1

# Crear el gráfico 3D interactivo
fig = go.Figure(data=[go.Scatter3d(
    x=X1,  # Característica 1 en el eje X
    y=X2,  # Característica 2 en el eje Y (valores constantes en 0)
    z=predictions_ridge_1,  # Predicciones en el eje Z
    mode='markers',
    marker=dict(
        size=5,
        color=predictions_ridge_1,  # Color basado en las predicciones
        colorscale='Viridis',  # Escala de color
        opacity=0.8
    )
)])

# Configurar etiquetas y título
fig.update_layout(
    scene=dict(
        xaxis_title='Característica 1 (X2)',
        yaxis_title='Característica 2 (Constante 0)',
        zaxis_title='Valor Objetivo (Predicción)'
    ),
    title='Gráfico de dispersión 3D interactivo'
)

# Mostrar el gráfico
fig.show()

# Realizar la predicción
predictions_ridge_2 = trained_ridge_2.predict(df_cuadricula)

# Mostrar las predicciones
print("Predicciones para los nuevos datos:")
print(predictions_ridge_2)

import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Extraer la característica 'X2' del DataFrame
X1 = df_cuadricula['X2']

# Crear un vector de ceros del mismo tamaño que X1 para representar 'X2'
X2 = np.zeros(len(X1))  # Esto crea un array de ceros del mismo tamaño que X1

y_objetivo = predictions_ridge_2

# Crear el gráfico 3D interactivo
fig = go.Figure(data=[go.Scatter3d(
    x=X1,  # Característica 1 en el eje X
    y=X2,  # Característica 2 en el eje Y (valores constantes en 0)
    z=predictions_ridge_2,  # Predicciones en el eje Z
    mode='markers',
    marker=dict(
        size=5,
        color=predictions_ridge_2,  # Color basado en las predicciones
        colorscale='Viridis',  # Escala de color
        opacity=0.8
    )
)])

# Configurar etiquetas y título
fig.update_layout(
    scene=dict(
        xaxis_title='Característica 1 (X2)',
        yaxis_title='Característica 2 (Constante 0)',
        zaxis_title='Valor Objetivo (Predicción)'
    ),
    title='Gráfico de dispersión 3D interactivo'
)

# Mostrar el gráfico
fig.show()

# Realizar la predicción
predictions_ridge_3 = trained_ridge_3.predict(df_cuadricula)

# Mostrar las predicciones
print("Predicciones para los nuevos datos:")
print(predictions_ridge_3)

import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Extraer la característica 'X2' del DataFrame
X1 = df_cuadricula['X2']

# Crear un vector de ceros del mismo tamaño que X1 para representar 'X2'
X2 = np.zeros(len(X1))  # Esto crea un array de ceros del mismo tamaño que X1

y_objetivo = predictions_ridge_3

# Crear el gráfico 3D interactivo
fig = go.Figure(data=[go.Scatter3d(
    x=X1,  # Característica 1 en el eje X
    y=X2,  # Característica 2 en el eje Y (valores constantes en 0)
    z=predictions_ridge_3,  # Predicciones en el eje Z
    mode='markers',
    marker=dict(
        size=5,
        color=predictions_ridge_3,  # Color basado en las predicciones
        colorscale='Viridis',  # Escala de color
        opacity=0.8
    )
)])

# Configurar etiquetas y título
fig.update_layout(
    scene=dict(
        xaxis_title='Característica 1 (X2)',
        yaxis_title='Característica 2 (Constante 0)',
        zaxis_title='Valor Objetivo (Predicción)'
    ),
    title='Gráfico de dispersión 3D interactivo'
)

# Mostrar el gráfico
fig.show()

# Realizar la predicción
predictions_ridge_4 = trained_ridge_4.predict(df_cuadricula)

# Mostrar las predicciones
print("Predicciones para los nuevos datos:")
print(predictions_ridge_4)

import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Extraer la característica 'X2' del DataFrame
X1 = df_cuadricula['X2']

# Crear un vector de ceros del mismo tamaño que X1 para representar 'X2'
X2 = np.zeros(len(X1))  # Esto crea un array de ceros del mismo tamaño que X1

y_objetivo = predictions_ridge_4

# Crear el gráfico 3D interactivo
fig = go.Figure(data=[go.Scatter3d(
    x=X1,  # Característica 1 en el eje X
    y=X2,  # Característica 2 en el eje Y (valores constantes en 0)
    z=predictions_ridge_4,  # Predicciones en el eje Z
    mode='markers',
    marker=dict(
        size=5,
        color=predictions_ridge_4,  # Color basado en las predicciones
        colorscale='Viridis',  # Escala de color
        opacity=0.8
    )
)])

# Configurar etiquetas y título
fig.update_layout(
    scene=dict(
        xaxis_title='Característica 1 (X2)',
        yaxis_title='Característica 2 (Constante 0)',
        zaxis_title='Valor Objetivo (Predicción)'
    ),
    title='Gráfico de dispersión 3D interactivo'
)

# Mostrar el gráfico
fig.show()

# Realizar la predicción
predictions_ridge_5 = trained_ridge_5.predict(df_cuadricula)

# Mostrar las predicciones
print("Predicciones para los nuevos datos:")
print(predictions_ridge_5)

import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Extraer la característica 'X2' del DataFrame
X1 = df_cuadricula['X2']

# Crear un vector de ceros del mismo tamaño que X1 para representar 'X2'
X2 = np.zeros(len(X1))  # Esto crea un array de ceros del mismo tamaño que X1

y_objetivo = predictions_ridge_5

# Crear el gráfico 3D interactivo
fig = go.Figure(data=[go.Scatter3d(
    x=X1,  # Característica 1 en el eje X
    y=X2,  # Característica 2 en el eje Y (valores constantes en 0)
    z=predictions_ridge_5,  # Predicciones en el eje Z
    mode='markers',
    marker=dict(
        size=5,
        color=predictions_ridge_5,  # Color basado en las predicciones
        colorscale='Viridis',  # Escala de color
        opacity=0.8
    )
)])

# Configurar etiquetas y título
fig.update_layout(
    scene=dict(
        xaxis_title='Característica 1 (X2)',
        yaxis_title='Característica 2 (Constante 0)',
        zaxis_title='Valor Objetivo (Predicción)'
    ),
    title='Gráfico de dispersión 3D interactivo'
)

# Mostrar el gráfico
fig.show()

# Realizar la predicción
predictions_ridge_6 = trained_ridge_6.predict(df_cuadricula)

# Mostrar las predicciones
print("Predicciones para los nuevos datos:")
print(predictions_ridge_6)

import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Extraer la característica 'X2' del DataFrame
X1 = df_cuadricula['X2']

# Crear un vector de ceros del mismo tamaño que X1 para representar 'X2'
X2 = np.zeros(len(X1))  # Esto crea un array de ceros del mismo tamaño que X1

y_objetivo = predictions_ridge_6

# Crear el gráfico 3D interactivo
fig = go.Figure(data=[go.Scatter3d(
    x=X1,  # Característica 1 en el eje X
    y=X2,  # Característica 2 en el eje Y (valores constantes en 0)
    z=predictions_ridge_6,  # Predicciones en el eje Z
    mode='markers',
    marker=dict(
        size=5,
        color=predictions_ridge_6,  # Color basado en las predicciones
        colorscale='Viridis',  # Escala de color
        opacity=0.8
    )
)])

# Configurar etiquetas y título
fig.update_layout(
    scene=dict(
        xaxis_title='Característica 1 (X2)',
        yaxis_title='Característica 2 (Constante 0)',
        zaxis_title='Valor Objetivo (Predicción)'
    ),
    title='Gráfico de dispersión 3D interactivo'
)

# Mostrar el gráfico
fig.show()