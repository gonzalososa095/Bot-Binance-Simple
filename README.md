# Bot-Binance-Simple
Bot para hacer trading en Binance que trabaja con bandas de Bollinger y RSI 

## Requerimientos

Se debe sincronizar el reloj de internet con time.nist.gov

```
pip install python-binance
```
Documentación : https://python-binance.readthedocs.io/en/latest/index.html

## Forma de uso

El Bot trabaja en base a las bandas de Bollinger y al RSI en velas de 15 minutos.
Las condiciones de trabajo son las siguientes:

- El Bot registra el último Trade del simbolo que se quiera trabajar. Extrae la información de si fue venta o compra, de la cantidad y el precio.
- El primer trade que haga el Bot va a ser de tipo opuesto al que se haya realizado anteriormente. Es decir si el último fue compra, el que haga será venta.
- La orden se genera siempre y cuando la relación entre el trade que se quiere hacer y el anterior deje una ganancia mayor a la comisión de Binance.
- La cantidad del simbolo a trabajar se basa en el anterior trade. Si el anterior trade fue de compra, el bot va a vender esa cantidad que se compro.
- Si nunca se realizó un Trade con el simbolo que se quiere trabajar se debe ingresar la cantidad que se pretende usar para el trade en la sección del simbolo de
Bot_15.py, Además se debe agregar un trade "ficticio" como se muestra a continuación: 


```
else:
    UltimaOrdenBTC = [{'status':'FILLED','side':'BUY','price':'9628.84'}] 
    RegistroOrdenesBTC.append(UltimaOrdenBTC)
```
En 'side' se pone el tipo de la última transacción, 'BUY' para compra 'SELL' para venta. En price se pone el precio. Para el ejemplo, como la orden es de compra,
el primer Trade que realice el Bot va a ser de venta. 

## Limitaciones

El Bot frena por problemas de conexión o por que se desincroniza el reloj.

