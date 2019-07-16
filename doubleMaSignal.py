# -*- coding: UTF-8 -*-

import talib as ta
import numpy as np
import pandas as pd

"""
将kdj策略需要用到的信号生成器抽离出来
"""

class maSignal():

    def __init__(self):
        self.author = 'Yixuan'

    def maEnvironment(self, am, paraDict):
        envPeriod = paraDict["envPeriod"]

        envMa = ta.MA(am.close, envPeriod)
        envDirection = 1 if am.close[-1]>envMa[-1] else -1
        return envDirection, envMa

    def maCross(self,am,paraDict):
        fastPeriod = paraDict["fastPeriod"]
        slowPeriod = paraDict["slowPeriod"]
        
        sma = ta.MA(am.close, fastPeriod)
        lma = ta.MA(am.close, slowPeriod)



        fastPeriod2 = 6    
        slowPeriod2 = 12    
        signalPeriod = 9

        macd,macdSignal,macdhist = ta.MACD(am.close, fastPeriod2, slowPeriod2, signalPeriod)
        
        long = macd[-1]>0 and macd[-11]<0 and macd[-1]>macd[-11] and macdSignal[-1]>macdSignal[-8]
        short = macd[-1]<0 and macd[-11]>0 and macd[-1]<macd[-11] and macdSignal[-1]<macdSignal[-8]

        goldenCross = sma[-1]>lma[-1] and sma[-2]<=lma[-2]
        deathCross = sma[-1]<lma[-1] and sma[-2]>=lma[-2]

        maCrossSignal = 0

        if goldenCross and long == 1 :
            maCrossSignal = 1
        elif deathCross and long == 0:
            maCrossSignal = -1
        else:
            maCrossSignal = 0
        return maCrossSignal, sma, lma