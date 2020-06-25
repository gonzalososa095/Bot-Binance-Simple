# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 12:48:59 2020

@author: Gonzalo Sosa
"""
from binance.client import Client
import numpy as np
import Operaciones


#Ingresar api generada en binance 
api_key = ''
api_secret = ''
clientUser = Client(api_key, api_secret,{"verify": True, "timeout": 20})



#Agregar los simbolos con los que se quiera trabajar de forma análoga a:
################################################################
Symbol1 = "BTCUSDT"
CantidadBTC = 0.010023 
RegistroOrdenesBTC = []
tradesBTC = clientUser.get_my_trades(symbol='BTCUSDT',limit=2)

if len(tradesBTC) > 0:
    PriceBTC = np.str(tradesBTC[-1]["price"])
    BuyerBTC = tradesBTC[-1]["isBuyer"]
    QtyBTC = tradesBTC[-1]["qty"]
    if BuyerBTC ==True:
        sideBTC = 'BUY'
        CantidadBTC = np.around(np.float16(QtyBTC),6)
    else:
        sideBTC='SELL'
        CantidadBTC = np.around(np.float16(QtyBTC),6)

    UltimaOrdenBTC = [{'status':'FILLED','side':sideBTC,'price':PriceBTC}]
    RegistroOrdenesBTC.append(UltimaOrdenBTC)
else:
    UltimaOrdenBTC = [{'status':'FILLED','side':'BUY','price':'9628.84'}]
    RegistroOrdenesBTC.append(UltimaOrdenBTC)
    

#############################################################
Symbol2 = "ETHUSDT"
CantidadETH = 0.07
RegistroOrdenesETH = []
tradesETH = clientUser.get_my_trades(symbol='ETHUSDT',limit=2)

if len(tradesETH) > 0:
    
    PriceETH = np.str(tradesETH[-1]["price"])
    BuyerETH = tradesETH[-1]["isBuyer"]
    QtyETH = tradesETH[-1]["qty"]
    
    if BuyerETH == True:
        sideETH = 'BUY'
        CantidadETH = np.around(np.float16(QtyETH),6)
    else:
        sideETH = 'SELL'
        CantidadETH = np.around(np.float16(QtyETH),6)

    UltimaOrdenETH = [{'status':'FILLED','side':sideETH,'price':PriceETH}]
    RegistroOrdenesETH.append(UltimaOrdenETH)
else:
    UltimaOrdenETH = [{'status':'FILLED','side':'BUY','price':'235'}]
    RegistroOrdenesETH.append(UltimaOrdenETH)
    

#############################################################


Horas = 24
TiempoSleep = 1 
HorasParametro = np.int(Horas * 3600 / TiempoSleep)

for i in range(HorasParametro):
    
    
    ActualPriceBTC, bollUPBTC, bollDOWNBTC, RsiBTC = Operaciones.Operaciones(Symbol1,clientUser,RegistroOrdenesBTC,CantidadBTC)
    
    ActualPriceETH, bollUPETH, bollDOWNETH, RsiETH = Operaciones.Operaciones(Symbol2,clientUser,RegistroOrdenesETH,CantidadETH)
           

        
   
