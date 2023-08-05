# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 19:37:12 2017

@author: cpkmanchee

Notes:

Prism pair - double pass!
Simulate prism pair
pulse = input pulse object
L = prism separation (m)

AOI = angle of incidence (deg)


"""

import numpy as np
from beamtools.constants import h,c
import sympy as sym


def disp_coef(L, AOI, np, eps, lambda0, disp_order=5):
    '''Calculate prism dispersion coefficents symbolically.
    This will be diffucultsssss.

    '''
    orders = disp_order
    a = AOI*np.pi/180    #convert AOI into rad

    w0 = 2*np.pi*c/lambda0
    #theta = np.arcsin(m*2*np.pi*c/(w0*d) - np.sin(g))
    w = sym.symbols('w')  

    phi = np.zeros(orders)
    
    for i in range(orders):
        phi[i] = sym.diff(phi0,w,i).subs(w,w0)
        
    return phi