#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 10:19:31 2022
"""
import pandas,datetime
import glob,os,re
import numpy as np
from scipy.stats import ttest_ind
from matplotlib import pyplot as pl

#%% union list
gsulist=pandas.read_csv('gsulist.csv')
unions=list(gsulist.list.str.lower())
unions.extend(gsulist.alt.str.lower())
unions.extend(gsulist.alt2.str.lower())


#%%
og=pandas.read_csv('phdstipends.csv')
og.Department.isna()
df=og[~og.Department.isna()]
df.Department=df.Department.str.lower()

#%%

pat='|'.join(map(re.escape, ['engineering','mathematics','medical' \
                             ,'bio','chem','physic','computer', \
                                 'neuro','statistic', 'genetic']))
df_stem=df[df.Department.str.contains(pat)]
df_stem['STEM']=True

pat='|'.join(map(re.escape, ['history','english','philosophy' \
                             ,'sociology','music','art ','study','education', \
                                 'literature','french','german','spanish','design', \
                                     'politic','policy','social']))
df_ns=df[df.Department.str.contains(pat)]

df_ns['STEM']=False


D=pandas.concat([df_stem,df_ns])
D=D.iloc[:,[0,1,2,11]]
D.University=D.University.str.lower()
D=D.dropna()

pat='|'.join(map(re.escape, unions))
D['Union']=D.University.str.contains(pat)
D['Overall Pay']=D['Overall Pay'].str.replace(',','')
D['pay']=D['Overall Pay'].str.replace('$','').astype(int)
D=D[(D.pay<100000)&(D.pay>5000)]


#%%
bs=1000

pl.figure(figsize=(10,4))
x=D.pay[D.STEM]
h=np.histogram(x,np.arange(0,100000,bs),density=False)
pl.plot(h[1][:-1],h[0],':',color='k',label='COmbined')
x=D.pay[D.STEM&D.Union]
h=np.histogram(x,np.arange(0,100000,bs),density=False)
pl.plot(h[1][:-1],h[0],'k',label='With Union')
x=D.pay[D.STEM&~D.Union]
h=np.histogram(x,np.arange(0,100000,bs),density=False)
pl.plot(h[1][:-1],h[0],color='#999999',label='Without Union')
pl.xlim(0,80000)
pl.xlabel('Stipend (USD)')
pl.ylabel('Count')
pl.legend()
pl.title('STEM Departments')

# pl.savefig('stipdent1.pdf')



pl.figure(figsize=(10,4))

x=D.pay[~D.STEM]
h=np.histogram(x,np.arange(0,100000,bs),density=False)
pl.plot(h[1][:-1],h[0],':',color='k',label='Combined')
x=D.pay[~D.STEM&D.Union]
h=np.histogram(x,np.arange(0,100000,bs),density=False)
pl.plot(h[1][:-1],h[0],'k',label='With Union')
x=D.pay[~D.STEM&~D.Union]
h=np.histogram(x,np.arange(0,100000,bs),density=False)
pl.plot(h[1][:-1],h[0],color='#999999',label='Without Union')
pl.xlim(0,80000)
pl.legend()
pl.title('non-STEM Departments')

# df=sum(D.STEM)-2
# t,p=ttest_ind(D.pay[D.STEM&D.Union],D.pay[D.STEM&~D.Union])
# pl.text(35000,80,'Union effect (STEM): T(%.0f)=%.1f, p=%.1e'%(df,t,p))

# df=sum(~D.STEM)-2
# t,p=ttest_ind(D.pay[~D.STEM&D.Union],D.pay[~D.STEM&~D.Union])
# pl.text(35000,70,'Union effect (none-STEM): T(%.0f)=%.1f, p=%.1e'%(df,t,p))

# df=len(D)-2
# t,p=ttest_ind(D.pay[D.STEM],D.pay[~D.STEM])
# pl.text(35000,60,'STEM effect (regardless of Union): T(%.0f)=%.1f, p=%.1e'%(df,t,p))

pl.xlabel('Stipend (USD)')
pl.ylabel('Count')

# pl.savefig('stipdent2.pdf')

#%%
import statsmodels.api as sm
from statsmodels.formula.api import ols

#perform two-way ANOVA
model = ols('pay ~ C(Union) + C(STEM) + C(Union):C(STEM)', data=D).fit()
sm.stats.anova_lm(model, typ=2)


