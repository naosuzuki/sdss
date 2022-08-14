import fitsio
import sys
import os
import pandas as pd
pylibdir=os.environ['PYLIB']
sys.path.append(pylibdir)
import sdss_catalog
import sdss_db

githubdir=os.environ['GITHUB_DIR']
gaiacsvdir=githubdir+'projects_gaia/csvfiles/'

objtype=sys.argv[1]

#spall=sdss_catalog.spall()
#print(spall.dr)
#print(spall.fitstablename)
#spall.read()

# Star
#objtype='star'
if(objtype=='star'):
   flag_gaia=True
   csvfile=gaiacsvdir+'gaiadr3_sdssdr8_star.csv'
   csvfile=gaiacsvdir+'gaiadr3_sdssdr17_star.csv'
   df=pd.read_csv(csvfile)
   print(df)
   dfstar=df.copy()
   #dfwd=dfstar[((dfstar['subclass']=='WDhotter') | \
   #            (dfstar['subclass']=='WDcooler') | \
   #            (dfstar['subclass']=='WDmagnetic') | \
   #            (dfstar['subclass']=='CalciumWD'))]
   dfwd=dfstar[dfstar['subclass'].str.contains('WD')]
   dfspec=dfwd.sort_values(by=['teff'],ascending=False)
   dfspec.reset_index()

   dfstar2=dfstar[((dfstar['subclass']!='WDhotter') | \
               (dfstar['subclass']!='WDcoller') | \
               (dfstar['subclass']!='WDmagnetic') | \
               (dfstar['subclass']!='WD') | \
               (dfstar['subclass']!='CalciumWD'))]
   dfspec2=dfstar2.sort_values(by=['teff'],ascending=False)
   dfspec2.reset_index()

   print('dfwd=',dfwd)
   print('dfspec=',dfspec)
   #for i in range(1000):
   for i in range(len(dfspec)):
    plate=dfspec['plate'].iloc[i]
    mjd  =dfspec['mjd'].iloc[i]
    fiber=dfspec['fiber'].iloc[i]
    #print(i,plate,mjd,fiber)
    print(i,plate,mjd,fiber,dfspec['subclass'].iloc[i],dfspec['teff'].iloc[i])

   fitsfilename='sdssDR17_wd.fits'
   sdss_db.create_2dspec(dfspec,fitsfilename,objtype,flag_gaia)

   print('dfspec2=',dfspec2)
   #for i in range(100,200):
   for i in range(len(dfspec2)):
    plate=dfspec2['plate'].iloc[i]
    mjd  =dfspec2['mjd'].iloc[i]
    fiber=dfspec2['fiber'].iloc[i]
    print(i,plate,mjd,fiber)
    print(i,plate,mjd,fiber,dfspec2['subclass'].iloc[i],dfspec2['teff'].iloc[i])

   fitsfilename='sdssDR17_star.fits'
   sdss_db.create_2dspec(dfspec2,fitsfilename,objtype,flag_gaia)
   del dfwd ; del dfstar ; del df ; del dfspec ; del dfspec2

# Galaxy
#objtype='galaxy'
if(objtype=='galaxy'):
   csvfile='../csvfiles/v5_13_2_spall_galaxy.csv'
   df=pd.read_csv(csvfile)
   print(df)
   #df['class']=df['class'].str.strip()
   #df['subclass']=df['subclass'].str.strip()
   #dfgalaxy=df[(df['class']=='GALAXY') & (df['thing_id']!=-1)]
   dfgalaxy=df.copy()
   #print(dfgalaxy)
   dfspec=dfgalaxy.sort_values(by=['z'],ascending=False)

   fitsfilename='sdssDR17_galaxy.fits'
   flag_gaia=False
   sdss_db.create_2dspec(dfspec,fitsfilename,objtype,flag_gaia)
   del dfgalaxy ; del dfspec ; del df

# Quasar
#objtype='quasar'
if(objtype=='quasar'):
   csvfile='../csvfiles/v5_13_2_spall_quasar.csv'
   df=pd.read_csv(csvfile)
   print(df)
   dfquasar=df.copy()
   #df['class']=df['class'].str.strip()
   #df['subclass']=df['subclass'].str.strip()
   #dfquasar=df[(df['class']=='QSO   ') & (df['thing_id']!=-1)]
   #dfquasar=df[(df['class']=='QSO') & (df['thing_id']!=-1)]
   #print(dfgalaxy)
   dfspec=dfquasar.sort_values(by=['z'],ascending=False)

   fitsfilename='sdssDR17_quasar.fits'
   flag_gaia=False
   sdss_db.create_2dspec(dfspec,fitsfilename,objtype,flag_gaia)
   #del products_list ; del df ; del dfquasar
   del df ; del dfquasar ;  del dfspec
