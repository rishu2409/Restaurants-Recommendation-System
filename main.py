#from IPython.display import HTML
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt         # For Exploratory Data Analysis
#matplotlib inline
import seaborn as sns           # For Exploratory Data Analysis
import plotly                             # For Exploratory Data Analysis
import plotly.express as px
import plotly.graph_objs as go
from geopy.geocoders import Nominatim     # geopy makes it easy for Python developers to locate the coordinates of addresses, cities, countries, and landmarks across the globe using third-party geocoders and other data sources
#import folium                         # To depict the map
#from folium.plugins import HeatMap
#from folium.plugins import FastMarkerCluster
#from plotly import tools
import re
from plotly.offline import init_notebook_mode, plot, iplot
#from wordcloud import WordCloud, STOPWORDS                      # To visualize the most and least popular words
from warnings import filterwarnings                 # To ignore the unnecessary warnings.
filterwarnings('ignore')
#np.set_printoptions(threshold=np.Infinity)


df = pd.read_csv(r'C:\Users\rshah39\Desktop\Fall 2022\CIS 5100\Project\zomato.csv')

#print(df.head())

#df.info()

df.isnull().sum() 

#df.describe()


locations = pd.DataFrame({'Name':df['location'].unique()})

#print(locations.head())

geolocator = Nominatim(user_agent='app')

lat = []
lon = []
for location in locations['Name']:
  location = geolocator.geocode(location)
  if location is None:
    lat.append(np.nan)
    lon.append(np.nan)
  else:
    lat.append(location.latitude)
    lon.append(location.longitude)

locations['lat'] = lat
locations['lon'] = lon

#print(locations.head())

rest_locat = pd.DataFrame(df['location'].value_counts().reset_index())

rest_locat.columns = ['Name', 'count']
#print(rest_locat.head())

#print(locations.shape)
#print(rest_locat.shape)

rest_locat = rest_locat.merge(locations, on='Name', how='left').dropna()
#print(rest_locat.head())


df.dropna(axis=0, subset=['rate'], inplace=True)
#print(df['rate'].unique())


def split(x):
  return x.split('/')[0]


df['rating'] = df['rate'].apply(split)
df['rating'].unique()

df.replace('NEW', 0, inplace=True)
df.replace('-', 0, inplace=True)

df['rating'] = pd.to_numeric(df['rating'])
#print(df.groupby(['location'])['rating'].mean().sort_values(ascending=False))

df.groupby(['location'])['rating'].mean()

avg_rating = df.groupby(['location'])['rating'].mean().values
loc = df.groupby(['location'])['rating'].mean().index
geolocator = Nominatim(user_agent='app')
lat = []
lon = []
for location in loc:
  location = geolocator.geocode(location)
  if location is None:
    lat.append(np.nan)
    lon.append(np.nan)
  else:
    lat.append(location.latitude)
    lon.append(location.longitude)
rating = pd.DataFrame()
rating['location'] = loc
rating['lat'] = lat
rating['lon'] = lon
rating['avg_rating'] = avg_rating

#print(rating.head())
rating.isna().sum()
rating = rating.dropna()
while(True):
  print(df['cuisines'].unique())
  print('Enter the tpe of cuisine you would like to have today: ')
  ty = input()
  df2 = df[df['cuisines'] == '{}'.format(ty)]
  print(df2.loc[:,["name", "rating"]])
