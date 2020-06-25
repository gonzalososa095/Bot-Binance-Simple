# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 13:10:16 2020

@author: Gonzalo
"""
import numpy as np
def CalculoRsi(ValoresCierre):
    vector = -1 * np.arange(1,15)
    x = ValoresCierre
    Alza = []
    Baja = []
    Total = []
    for i in vector:
        resta = x[i]-x[i-1]
        Total.append(resta)
        if resta < 0:
            Baja.append(np.abs(resta))
        else:
            Alza.append(resta)

    MediaAlza = np.sum(Alza) / 14
    MediaBaja = np.sum(Baja) / 14
    Rs = MediaAlza / MediaBaja

    Rsi = np.around(100 - 100/(1+Rs),2)
    
    return Rsi,Total



    
    

    


