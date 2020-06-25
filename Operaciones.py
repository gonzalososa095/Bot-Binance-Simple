# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 18:35:52 2020

@author: Gonzalo
"""
from binance.client import Client
import numpy as np
import CalculoRsi




def Operaciones(symbol,client,RegistroOrdenes,cantidad):
    
    clientGonza = client
    sell = False
    buy = False
    OpenOrders = clientGonza.get_open_orders(symbol=symbol)
    L = len(OpenOrders)
    
    
    feesSell = 1.002
    feesBuy = 0.998
    
    if L == 1:   
        Tipo = OpenOrders[0]["side"]
        #OrderId = np.str(OpenOrders[0]["orderId"])
        if Tipo == "SELL":
            sell = True
            #price = np.float(OpenOrders[0]["price"])
        else:
            if Tipo == "BUY":
                buy = True
                #price = np.float(OpenOrders[0]["price"])
    else:
        if L == 0:
            sell = False
            buy = False
    
    
    klines = clientGonza.get_historical_klines(symbol, Client.KLINE_INTERVAL_15MINUTE, "300 minute ago UTC")
    #time.sleep(TiempoSleep)    
    ValoresCierre = []
    
    for j in range(len(klines)):
    
        ValoresCierre.append(np.float(klines[j][1]))
    
    tickers = clientGonza.get_ticker(symbol=symbol)
    ActualPrice = np.float(tickers['askPrice'])
    
    ValoresCierre.append(ActualPrice)
    
    Promedio = np.mean(ValoresCierre)
    Desvio = np.std(ValoresCierre)
    
    bollUP = Promedio + Desvio*2
    bollUPHigh = np.around(bollUP*1.00108,2)
    bollUPLow = np.around(bollUP*0.99892,2)
    bollDOWN = Promedio - Desvio*2
    bollDOWNLow = np.around(bollDOWN*0.99892,2)
    bollDOWNUp = np.around(bollDOWN*1.00108,2)
    
    Rsi , Total = CalculoRsi.CalculoRsi(ValoresCierre)
    
    RangoBollinger = bollUP / bollDOWN
    
    
    if RangoBollinger > 1.001:
        if sell == False and buy == False:
            
            if (ActualPrice > bollUP and Rsi>70) or (ActualPrice > bollUPHigh and Rsi>60) or (Rsi > 90 and ActualPrice > bollUPLow):
                #Place a limit order to sell en sellPrice
                sellPrice = ActualPrice
                sellPrice = np.around(sellPrice,2)
                sellPrice1 = sellPrice
                sellPrice = np.str(sellPrice)
                
                #ChequeoTipo = Chequeo[0]["side"]
                #ChequeoStatus = Chequeo[0]["status"]
                if len(RegistroOrdenes) > 0:
                    Last = RegistroOrdenes[-1]
                    LastStatus = Last[0]["status"] 
                    LastTipo = Last[0]["side"]
                    LastPrice = np.around(np.float(Last[0]["price"]),2)
                    LastPriceFees = np.around(LastPrice*feesSell,2)
                    if LastStatus == 'FILLED' and LastTipo == 'BUY' and sellPrice1>LastPriceFees:
                        clientGonza.order_limit_sell(symbol=symbol,
                                                 quantity=cantidad,
                                                 price=sellPrice)
                        ObtencionID = clientGonza.get_all_orders(symbol=symbol,limit=1)
                        RegistroOrdenes.append(ObtencionID)
                        print("Se genero una orden de venta por: ",sellPrice)
                else:
                    
                    clientGonza.order_limit_sell(symbol=symbol,
                                                          quantity=cantidad,
                                                          price=sellPrice)
                    ObtencionID = clientGonza.get_all_orders(symbol=symbol, limit=1)
                    RegistroOrdenes.append(ObtencionID)
                    print("Se genero una orden de venta por: ",sellPrice)
            else:
                if (ActualPrice < bollDOWN and Rsi<30)  or (ActualPrice < bollDOWNLow and Rsi < 40) or (Rsi < 10 and ActualPrice < bollDOWNUp):
                    #place a limit order to buy en bolldown + k%
                    buyPrice = ActualPrice
                    buyPrice = np.around(buyPrice,2)
                    buyPrice1 = buyPrice
                    buyPrice = np.str(buyPrice)
                    if len(RegistroOrdenes) > 0:
                        Last = RegistroOrdenes[-1]
                        LastStatus = Last[0]["status"] 
                        LastTipo = Last[0]["side"]
                        LastPrice = np.around(np.float(Last[0]["price"]),2)
                        LastPriceFees = np.around(LastPrice*feesBuy,2)
                        cantidad = np.around(cantidad * (LastPrice/buyPrice1),6)
                        if LastStatus == 'FILLED' and LastTipo == 'SELL' and buyPrice1 < LastPriceFees :
                            clientGonza.order_limit_buy(symbol=symbol,
                                                 quantity=cantidad,
                                                 price=buyPrice)
                            ObtencionID = clientGonza.get_all_orders(symbol=symbol,limit=1)
                            RegistroOrdenes.append(ObtencionID)
                            print("Se genero una orden de compra por: ",buyPrice)
                    else:
                    
                        clientGonza.order_limit_buy(symbol=symbol,
                                                     quantity=cantidad,
                                                     price=buyPrice)
                        ObtencionID = clientGonza.get_all_orders(symbol=symbol, limit=1)
                        RegistroOrdenes.append(ObtencionID)
                        print("Se genero una orden de compra por: ",buyPrice)
    
    return ActualPrice, bollUP,bollDOWN,Rsi