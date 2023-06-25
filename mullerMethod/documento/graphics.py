import base64
import io

import matplotlib.pyplot as plt
import numpy as np
from sympy import *

class Graphics:
    def __init__(self, xValues, yValues, fx):
        self._x = xValues
        self._y = yValues
        self._fx = str(fx)

    def createGraphics(self):
        fig, graphics = plt.subplots()
        x = np.linspace(min(self._x), max(self._x), 100)
        y = eval(self._fx)

        #Puntos que se acercan a la raiz:
        graphics.scatter(self._x, self._y, color="green")
        graphics.plot(x, y, color="red", label="fx")

        # Agregar las coordenadas a cada punto
        for i, (x, y) in enumerate(zip(self._x, self._y)):
            label = f'({x:.2f}, {y:.2f})'  # Formateo de cadena para mostrar solo dos decimales
            graphics.annotate(label, (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

        plt.title(self._fx)
        plt.grid()

        # Creamos el archivo
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        # codificamos la imagen
        image64 = base64.b64encode(buffer.getvalue()).decode()

        return image64

    def graficaEcuacion(self, funcion):


        # Definir la función en Sympy
        x = symbols('x')

        raices = solve(funcion, x)

        raices.sort()

        rangoNumeros = 6
        minimo = min(raices) - rangoNumeros if min(raices) <= 0 else + rangoNumeros
        maximo = max(raices) + rangoNumeros

        minimo = int(minimo)
        maximo = int(maximo)

        print(raices, type(minimo), maximo)

        # Convertir la función de Sympy en una función numérica
        funcion_numpy = lambdify(x, funcion, 'numpy')

        # Crear un array de valores de x
        x_vals = np.linspace(minimo, maximo)

        # Evaluar la función en los valores de x
        y_vals = funcion_numpy(x_vals)

        # Graficar la función
        plt.plot(x_vals, y_vals)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid()
        plt.title('Gráfico de la función')

        for i in raices:
            plt.plot(i, funcion.subs(x, i), "ro")

            # Creamos el archivo
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            # codificamos la imagen
            image64 = base64.b64encode(buffer.getvalue()).decode()

            return image64
