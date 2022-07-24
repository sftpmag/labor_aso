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
if os.path.basename(os.getcwd())!='mcdonald_tomasula':
    os.chdir('/Users/catbox/Downloads/labor_aso/mcdonald_tomasula')
files=glob.glob('*.xlsx')

strikes=pandas.read_excel(files[0],sheet_name=0)
strikes=strikes.iloc[:min(np.where(np.all(strikes.isnull(),1))[0]),:]

campaigns=pandas.read_excel(files[-1],sheet_name=0)
campaigns=campaigns.iloc[:min(np.where(np.all(campaigns.isnull(),1))[0]),:]

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
ND['sn']=ND.s/(np.max(ND.s)-np.min(ND.s))*200
ND['pn']=ND.p/(np.max(ND.s)-np.min(ND.s))*200
ND['ln']=ND.l/(np.max(ND.l)-np.min(ND.l))

ND['sn']=np.clip(ND['sn'],a_min=0,a_max=50)
ND['pn']=np.clip(ND['pn'],a_min=0,a_max=50)


ND=ND.sort_values(by='y',ascending=True)

#%
count=-1
pl.figure(figsize=(10,20))
for x in ND.iterrows():
    count+=1
    pl.plot([50,50+x[1].l],(count,count),'k-',lw=3)
    pl.plot(0,count,'wo',ms=x[1].sn,mfc='k')
    pl.plot(20,count,'wo',ms=x[1].pn,mfc='k')
    if x[1].sn>15:
        pl.text(0,count,str(round(x[1].s/1000))+'k',color='w',ha='center',va='center',fontsize=8)
    if x[1].pn>15:
        pl.text(20,count,str(round(x[1].p/1000))+'k',color='w',ha='center',va='center',fontsize=8)
    if x[1].ln>0.2:
        pl.text(np.median((50,50+x[1].l)),count+0.1,str(int(x[1].l))+' d',ha='center')
    pl.text(-30,count,x[1].y)
pl.xlim(-30,250)
pl.yticks(np.arange(0,len(ND)),ND.n)

pl.savefig('infog.pdf')



#%% campaign inforgraphic
tbl=campaigns
nd=[]
for x in tbl.iterrows():
    nd.append({'n':x[1].Union+'--'+x[1].Employer,'t':int(x[1].Year),'y0':int(x[1]['Bargaining Unit Size']), \
               'y1':int(x[1]['Yes Votes']),'y2':int(x[1]['No Votes'])})
ND=pandas.DataFrame.from_records(nd)
absent=ND.y0-(ND.y1+ND.y2)
ND['absent']=absent
#%%
count=0
pl.figure(figsize=(10,20))

for x in ND.iterrows():
    pl.barh(count,x[1].y1+x[1].absent/2,edgecolor='k',facecolor='k')
    pl.barh(count,x[1].absent/2,edgecolor='k',facecolor='w')
    if x[1].y1>1000:
        pl.text(x[1].y1/2+x[1].absent/2,count,x[1].y1,color='w',ha='center',fontsize=8,va='center')
    pl.barh(count,-x[1].y2-x[1].absent/2,edgecolor='k',facecolor='k')
    pl.barh(count,x[1].absent/-2,edgecolor='k',facecolor='w')
    if x[1].y2>1000:
        pl.text(-x[1].y2/2-x[1].absent/2,count,x[1].y2,color='#999999',ha='center',fontsize=8,va='center')
    pl.text(-6000,count,x[1].t,ha='center')
    if x[1].y1<x[1].y2:
        pl.text(7500,count,'*')
    count+=1
pl.xlim(-7000,15000)
pl.yticks(np.arange(0,len(ND)),ND.n)

pl.savefig('infog2.pdf')
    



