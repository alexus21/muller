import math

import numpy as np
import pandas as pd
from sympy import *


def getMullerData(request):
    equation = request.POST.get("getEquation")
    x0 = request.POST.get("getX0")
    x1 = request.POST.get("getX1")
    x2 = request.POST.get("getX2")
    marginError = request.POST.get("getMarginOfError")

    return np.array([x0, x1, x2, marginError])
