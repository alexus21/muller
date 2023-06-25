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

        self._dataDict = {}

        self._listaX0, self._listaX1, self._listaX2, self._listaE = [], [], [], []

        self._imagenGrafica = ""


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



    def iteraciones(self, dataOrGraphics):
        self._fx = sympify(self._fx)
        self._fx0 = self._fx.subs(self._x, self._x0)
        self._fx1 = self._fx.subs(self._x, self._x1)
        self._fx2 = self._fx.subs(self._x, self._x2)

        xValues = np.array([self._x0, self._x1, self._x2])
        fxValues = np.array([self._fx0, self._fx1, self._fx2])

        self._dataDict = {
                        "i": [],
                        "x0": [],
                        "x1": [],
                        "x2": [],
                        "x3": [],
                        "E": []
                    }

        bandera = True

        while self._errorActual > self._error:
            ex = self._errorActual
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

            self._dataDict["i"].append(self._iteracion)
            self._dataDict["x0"].append(self._x0)
            self._dataDict["x1"].append(self._x1)
            self._dataDict["x2"].append(self._x2)
            self._dataDict["x3"].append(self._x3)



            self._errorActual = abs((self._x3 - self._x2) / self._x3)

            self._dataDict["E"].append(self._errorActual)
            self._listaE.append(self._errorActual)

            self._listaX0.append([self._iteracion, round(self._x0, 5), round(self._x1, 5), round(self._x2, 5), str(round(self._errorActual * 100, 5)) + "%"])

            self._valoresIteracion()
            self._reiniciarValores()


        if bandera:
            #self.showInfo(self.dataDict)
            dataaa = [self._listaX0, self._listaX1, self._listaX2]
            if dataOrGraphics:
                return self._listaX0

            from mullerMethod.documento.graphics import Graphics
            g = Graphics(xValues, fxValues, self._fx)
            # g.createGraphics()
            return g.createGraphics()



    def sendValues(self, xValues, fxValues):

        from mullerMethod.documento.graphics import Graphics
        g = Graphics(xValues, fxValues, self._fx)
        #g.createGraphics()
        return g.createGraphics()

