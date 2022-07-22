#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 10:19:31 2022
"""
import pandas,datetime
import glob,os
import numpy as np
from matplotlib import pyplot as pl

#%%
if os.path.basename(os.getcwd())!='labor_aso':
    os.chdir(os.path.join(os.getcwd(),'Downloads','labor_aso'))
files=glob.glob('*.xlsx')

strikes=pandas.read_excel(files[0],sheet_name=0)
strikes=strikes.iloc[:min(np.where(np.all(strikes.isnull(),1))[0]),:]

campaigns=pandas.read_excel(files[-1],sheet_name=0)
campaigns=campaigns.iloc[:min(np.where(np.all(campaigns.isnull(),1))[0]),:]

#%% only pull top 10

srch=campaigns['Employer(s)'].str.contains('University')
tbl=campaigns[srch]
tbl=tbl.sort_values(by='Bargaining Unit Size',ascending=False)
tbl=tbl.iloc[:10,:-1]
tbl['Voter Turnout (%)']=round(tbl['Voter Turnout (%)'],3)*100
tbl.to_excel('table1.xlsx',index=False)

#%% strikes edit
tbl=strikes
D=[]
for x in tbl.iterrows():
    ll=x[1].Duration.find('week')
    if ll>=0:
        s=float(x[1].Duration[:ll])
        r=s*7
    ll=x[1].Duration.find('day')
    if ll>=0:
        s=float(x[1].Duration[:ll])
        r=s
    ll=x[1].Duration.find('month')
    if ll>=0:
        s=float(x[1].Duration[:ll])
        r=s*30
    if x[1].Duration=='??':
        r=np.nan        
    # print(x[1].Duration,'->',r)
    D.append(r)
    
    
tbl['Duration']=D

tbl.iloc[6,5]=1080
tbl.iloc[7,5]=1080


#%% strike inforgraphic
nd=[]
for x in tbl.iterrows():
    y=x[1]['Year(s) of Strike(s)']
    l=x[1]['Duration']
    s=x[1]['Bargaining Unit Size']
    if isinstance(s,str):
        s=np.nan
    p=x[1]['# of Strikers']
    if isinstance(p,str):
        p=np.nan
    nd.append({'n':x[1].iloc[0]+'--'+x[1].iloc[1],'y':y,'l':l,'s':s,'p':p})
ND=pandas.DataFrame.from_records(nd)
ND['sn']=ND.s/(np.max(ND.s)-np.min(ND.s))
ND['pn']=ND.p/(np.max(ND.s)-np.min(ND.s))
ND['ln']=ND.l/(np.max(ND.l)-np.min(ND.l))

ND=ND.sort_values(by='y',ascending=True)

#%%
count=-1
pl.figure(figsize=(10,20))
for x in ND.iterrows():
    count+=1
    pl.plot([50,50+x[1].l],(count,count),'k-',lw=3)
    pl.plot(0,count,'wo',ms=x[1].sn*50,mfc='k')
    pl.plot(20,count,'wo',ms=x[1].pn*50,mfc='k')
    if x[1].sn>0.3:
        pl.text(0,count,str(round(x[1].s/1000))+'k',color='w',ha='center',va='center',fontsize=8)
    if x[1].ln>0.2:
        pl.text(np.median((50,50+x[1].l)),count+0.1,str(int(x[1].l))+' d',ha='center')
    pl.text(-30,count,x[1].y)
pl.xlim(-30,250)
pl.yticks(np.arange(0,len(ND)),ND.n)

pl.savefig('infog.pdf')


        




