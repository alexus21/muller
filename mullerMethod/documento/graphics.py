import base64
import io

import matplotlib.pyplot as plt
import numpy as np
from sympy import *

from decimal import *

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
            if i == len(self._x) - 1: # Mostrar unicamente el ultimo valor
                label = f'({x:.4f}, {y:.4f})'  # Formateo de cadena para mostrar solo dos decimales
                graphics.annotate(label, (x, y), textcoords="offset points", xytext=(0, 10), ha='center')
                graphics.plot(x, y, marker='o', color='black')

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

    def crearGrafica(self, function):

        funcion = sympify(function)

        # Definir el símbolo x
        x = symbols('x')

        # Definir la ecuación
        #funcion = sympify("x**3 -125")

        # Encontrar las raíces
        raices = solve(funcion, x)

        # Mostrar solo la parte real de las raíces
        raices_reales = [re(raiz).evalf() for raiz in raices]
        raices_totales = [re(raiz).evalf() for raiz in raices if raiz.is_real]
        print(raices_reales)

        raices_reales.sort()
        raices_totales.sort()

        rangoNumeros = 6

        # # Filtrar las raíces reales mayores o iguales a cero y obtener valores numéricos
        # raices_positivas = [raiz.evalf() for raiz in raices if re(raiz).is_real]
        #
        # raices_positivas.sort()
        #
        # rangoNumeros = 6
        minimoX = min(raices_reales) - rangoNumeros
        maximoX = max(raices_reales) + rangoNumeros

        minimoX = int(minimoX)
        maximoX = int(maximoX)

        # Convertir la función de Sympy en una función numérica
        funcion_numpy = lambdify(x, funcion, 'numpy')

        # Crear un array de valores de x
        x_vals = np.linspace(minimoX, maximoX)

        # Evaluar la función en los valores de x
        y_vals = funcion_numpy(x_vals)

        # Graficar la función
        plt.plot(x_vals, y_vals)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid()
        plt.title(funcion)

        def formatear_numero(numero):
            numero_decimal = Decimal(numero)
            if numero_decimal % 1 == 0:
                return str(numero_decimal.to_integral_value())
            else:
                return "{:.2f}".format(numero_decimal).rstrip('0').rstrip('.')

        for i in raices_reales:
            x_value = i
            xx = formatear_numero(str(i))
            xx = str(xx)
            xx = float(xx)
            print(x_value)
            y_value = funcion.subs(x, i)
            if i in raices_totales:
                plt.plot(x_value, y_value, "ro")
                plt.text(xx, y_value, f'({xx}, {y_value})', ha='center', va='bottom', rotation=80)


        # Creamos el archivo
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        # codificamos la imagen
        image64 = base64.b64encode(buffer.getvalue()).decode()

        return image64

