



import QuantLib as ql
import math
import numpy as np
import pandas as pd


#data
maturity_date = ql.Date(8, 5, 2017)
spot_price = 50
strike_price = 52
volatility = 0.30 # the historical vols for a year
dividend_rate =  0.0
#163
option_type = ql.Option.Call

risk_free_rate = 0.05
day_count = ql.Actual365Fixed()
calendar = ql.UnitedStates()

calculation_date = ql.Date(8, 5, 2016)
ql.Settings.instance().evaluationDate = calculation_date



bs_opt(maturity_date,spot_price,strike_price,volatility,dividend_rate,option_type,risk_free_rate,day_count
          ,calendar,calculation_date)

def bs_opt(maturity_date,spot_price,strike_price,volatility,dividend_rate,option_type,risk_free_rate,day_count
          ,calendar,calculation_date):
    #payoff
    payoff = ql.PlainVanillaPayoff(option_type, strike_price)
    exercise = ql.EuropeanExercise(maturity_date)
    european_option = ql.VanillaOption(payoff, exercise)
    #process
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
    flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, risk_free_rate, day_count))
    dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, dividend_rate, day_count))
    flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, volatility, day_count))
    #price
    bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)
    european_option.setPricingEngine(ql.AnalyticEuropeanEngine(bsm_process))
    bs_price = european_option.NPV()
    return bs_price
    #print("The theoretical price is ", bs_price)



def get_explict_abc(r,q,spot,ds,sigma,dt):
    a=((r-q)*spot*ds+sigma*sigma*spot*spot)/((r+1/dt)*2*ds*ds)
    #
    b=(1/dt-(sigma*sigma*spot*spot/(ds*ds)))/(r+1/dt)
    c=(-(r-q)*spot*ds+sigma*sigma*spot*spot)/((r+1/dt)*2*ds*ds)
    #print(r,q,spot,ds,sigma,dt)
    #risk_free_rate,dividend_rate,spot_price,spot_price/20,volatility,0.01
    return a,b,c



def explict_cal(fup,fmed,fdown,r,q,spot,ds,sigma,dt):
    (a,b,c)=get_explict_abc(r,q,spot,ds,sigma,dt)
    price=a*fup+b*fmed+c*fdown
    #print(a,b,c,price,fup,fmed,fdown,a*fup,b*fmed,c*fdown)
    l=np.array([price,a,b,c,spot,fup,fmed,fdown,a*fup,b*fmed,c*fdown])
    return l



#Explict
#時間軸
M=101
#價格軸
N=21
spot=np.ones((M,N))
opt_price=np.zeros((N,M))
#價格上限
upboundary=100
lowboundary=0
#價格spot矩陣
ds=(upboundary-lowboundary)/(N-1)
dt=(maturity_date-calculation_date)/(365*(M-1))
a=np.linspace(upboundary,lowboundary,N)
b=a*spot
spot=np.transpose(b)
#payoff
for i in range(0,len(spot[:,M-1]),1):
    opt_price[i,M-1]=max(spot[i,M-1]-strike_price,0)
    #max(spot[i,M-1]-strike_price,0)
#上下限價格
for i in range(0,len(spot[0,:]),1):
    opt_price[0,i]=opt_price[0,M-1]
    opt_price[N-1,i]=opt_price[N-1,M-1]
l=[]
for i in range(M-2,-1,-1):
    for j in range(N-2,0,-1):
        print(i,j)
        opt_price[j,i]=explict_cal(opt_price[j-1,i+1],opt_price[j,i+1],opt_price[j+1,i+1],
                                   risk_free_rate,dividend_rate,spot[j,i],
                                   ds,volatility,dt)[0]
        d=explict_cal(opt_price[j+1,i+1],opt_price[j,i+1],opt_price[j-1,i+1],risk_free_rate,dividend_rate,spot[j,i],
                                   ds,volatility,dt)
        l.append(d)

pd.DataFrame(opt_price)
pd.DataFrame(l)
pd.DataFrame(spot)



