import math

import numpy as np
import pandas as pd
from sympy import *

class Muller:
    def __init__(self, fx, x0, x1, x2, error):
        self._fx = fx
        self._valoresIniciales = np.array([x0, x1, x2])
        self._error = error
        self._errorActual = 1

        self._x = symbols("x")

        self._s0, self._s1 = 0, 0

        self._fx0, self._fx1, self._fx2 = 0, 0, 0

        self._a, self._b, self._c = 0, 0, 0

        self._h0, self._h1 = 0, 0

        self._x0, self._x1, self._x2, self._x3 = x0, x1, x2, 0

        self._iteracion = 0

        self.dataDict = {}

        self.listaX0, self.listaX1, self.listaX2, self.listaE = [], [], [], []


    def _valoresImagen(self):
        # self._fx = sympify(self._fx)
        # self._fx0 = self._fx.subs(self._x, self._x0)
        # self._fx1 = self._fx.subs(self._x, self._x1)
        # self._fx2 = self._fx.subs(self._x, self._x2)
        pass

    def _valoresHi(self):
        self._h0 = self._x1 - self._x0
        self._h1 = self._x2 - self._x1

    def _valoresSigma(self):
        self._s0 = (self._fx1 - self._fx0) / self._h0
        self._s1 = (self._fx2 - self._fx1) / self._h1

    def _valoresEcuacion(self):
        self._a = (self._s1 - self._s0) / (self._h1 - self._h0)
        self._b = self._a * self._h1 + self._s1
        self._c = self._fx2

    def _reiniciarValores(self):
        self._x0 = self._x1
        self._x1 = self._x2
        self._x2 = self._x3
        self._x3 = 0

    def _valores(self):
        self._valoresImagen()
        self._valoresHi()
        self._valoresSigma()
        self._valoresEcuacion()

    def _valoresIteracion(self):
        print("x0: ", self._x0, ", f(x0): ", self._fx0)
        print("x1: ", self._x1, ", f(x1): ", self._fx1)
        print("x2: ", self._x2, ", f(x2): ", self._fx2)
        print("h0: ", self._h0)
        print("h1: ", self._h1)
        print("s0: ", self._s0)
        print("s1: ", self._s1)
        print("a: ", self._a)
        print("b: ", self._b)
        print("c: ", self._c)
        print("x3: ", self._x3)
        print("Error: ", self._errorActual)
        print("_"*40)



    def valoresTres(self):
        self.iteraciones()
        data = []

        data.append(self.dataDict["x0"])
        data.append(self.dataDict["x1"])
        data.append(self.dataDict["x2"])
        data.append(self.dataDict["E"])
        return data

    def iteraciones(self):
        self._fx = sympify(self._fx)
        self._fx0 = self._fx.subs(self._x, self._x0)
        self._fx1 = self._fx.subs(self._x, self._x1)
        self._fx2 = self._fx.subs(self._x, self._x2)

        xValues = np.array([self._x0, self._x1, self._x2])
        fxValues = np.array([self._fx0, self._fx1, self._fx2])

        self.dataDict = {
                        "i": [],
                        "x0": [],
                        "x1": [],
                        "x2": [],
                        "x3": [],
                        "E": []
                    }

        bandera = True

        while self._errorActual > self._error:
            self._iteracion += 1
            self._valores()

            if self._h1 == self._h0:
                print("Esta función no se puede operar por medio de este método")
                bandera = False
                break

            raiz = math.pow(self._b, 2) - 4 * self._a * self._c

            if raiz < 0:
                print("No se puede resolver esta ecuacion", self._iteracion)
                bandera = False
                break

            d = sqrt(raiz)
            e = 0

            if abs(self._b + d) > abs(self._b - d):
                e = self._b + d
            else:
                e = self._b - d

            self._x3 = self._x2 - (2 * self._c) / e


            if self._x3 == 0:
                print("Esta función no se puede operar por medio de este método")
                bandera = False


            fx3 = self._fx.subs(self._x, self._x3)
            xValues = np.append(xValues, self._x3)
            fxValues = np.append(fxValues, fx3)

            self.dataDict["i"].append(self._iteracion)
            self.dataDict["x0"].append(self._x0)
            self.dataDict["x1"].append(self._x1)
            self.dataDict["x2"].append(self._x2)
            self.dataDict["x3"].append(self._x3)



            self._errorActual = abs((self._x3 - self._x2) / self._x3)

            self.dataDict["E"].append(self._errorActual)
            self.listaE.append(self._errorActual)

            self.listaX0.append([self._x0, self._x1, self._x2, self._errorActual])

            self._valoresIteracion()
            self._reiniciarValores()


        if bandera:
            #self.sendValues(xValues, fxValues)
            #self.showInfo(self.dataDict)
            dataaa = [self.listaX0, self.listaX1, self.listaX2]
            return self.listaX0



    def sendValues(self, xValues, fxValues):

        import graphics
        g = graphics.Graphics(xValues, fxValues, self._fx)
        #g.createGraphics()
        g.graficaEcuacion(self._fx)

    def showInfo(self, dataDict):

        import showInfo as si
        df = pd.DataFrame(dataDict)
        s = si.ShowInfo(df)
        s.showIterationsInfo()

def main():
    funcion = input("Ingrese la función a evaluar -> ")
    x0 = float(input("Ingrese el valor de x0 -> "))
    x1 = float(input("Ingrese el valor de x1 -> "))
    x2 = float(input("Ingrese el valor de x2 -> "))
    error = float(input("Ingrese el valor de error mínimo -> "))

    muller = Muller(funcion, x0, x1, x2, error)
    muller.iteraciones()
