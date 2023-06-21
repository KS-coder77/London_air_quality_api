#!/usr/bin/env python
# coding: utf-8

# In[2]:


from IPython.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))

import requests
from pprint import pprint
import json

base_url = "http://api.erg.ic.ac.uk/AirQuality" 
#url = /Hourly/MonitoringIndex/SiteCode={SITECODE}/Json"
url = f"{base_url}/Information/Groups/Json"

print(url)

#"http://api.erg.ic.ac.uk/AirQuality/Daily/MonitoringIndex/GroupName={GROUPNAME}/Date={DATE}/Json"

r = requests.get(url = url)
# r.url

data = r.json()
print(data)


# In[3]:


import urllib


# In[4]:


urllib.parse.urlencode({"Date":"2023-06-14 00:00:00"})


# In[5]:


help(urllib.request)


# In[9]:


import csv
import pandas as pd
location="London"
url = base_url + f"/Information/MonitoringLocalAuthority/GroupName={location}/Json"
print(url)
r = requests.get(url = url) 
r.raise_for_status()
data = r.json()
ourdata=[]
csvheaders=["ID", "Authority", "Latitude", "Longitude"]

for key, value in data['LocalAuthorities'].items():
    for d in value:
        boroughs= [d['@LocalAuthorityCode'], d['@LocalAuthorityName'],d['@LaCentreLatitude'], d['@LaCentreLongitude']] 
        ourdata.append(boroughs)

FILEPATH = r"C:\Temp\london_air_quality.csv"

with open (FILEPATH, "w", encoding = "UTF8", newline = "") as file:
    writer = csv.writer(file)
    writer.writerow(csvheaders)
    writer.writerows(ourdata)

print("done!")
        


# In[10]:


data2 = pd.read_csv(r"C:\Temp\london_air_quality.csv")
data2


# In[11]:


#daily AQI readings for London 

#url = base_url + "/Daily/MonitoringIndex/Latest/GroupName={GroupName}/Json"
#date=urllib.parse.urlencode({"Date":"2023-06-14"})
#date="2023-06-14"
#Daily/MonitoringIndex/GroupName={location}/Date={date}/Json"
#url = base_url + f"/Daily/MonitoringIndex/Latest/GroupName={location}/Json"
#PARAMS = {"GroupName":"AroundLondon","Date":"2023-06-14 00:00:00"}
#print(data)
#print(type(data))

location = "London"
import urllib
#urllib.parse.urlencode({"Date":"2023-06-15 00:00:00"})
date=urllib.parse.urlencode({"Date":"2023-06-15"})
#date="2023-06-15"
#date=date
url = base_url + f"/Daily/MonitoringIndex/Latest/GroupName={location}/Json"

print(url)
r = requests.get(url = url) 
r.raise_for_status()
data = r.json()
pprint(data)


# In[ ]:





# In[12]:


type({'a':1}) == dict


# In[13]:


#AQI for sites around london

ddata = []
csvheaders = ["Date", "Authority Name", "AQI", "Pollutant Description", "Pollutant", "Site Name", "Site Code", "Site Type", "Latitude", "Longitude"]

for key, value in data['DailyAirQualityIndex'].items():
    for d in data['DailyAirQualityIndex']['LocalAuthority']:
       # print(d['@LocalAuthorityName'])
        #print(d.keys())
        if 'Site' in d:
            items = d['Site']
            if type(items) == dict:
                #print('isdict')
                items = [items]
            #print(d['Site'])
            
            for item in items:
                sitename = item['@SiteName']
                date = item['@BulletinDate']
                lat = item['@Latitude']
                long = item['@Longitude']
                sitetype = item['@SiteType']
                sitecode = item['@SiteCode']
                
                if "Species" in item:
                    #print(d['Site']['Species'])
                    species = item['Species']
                    
                    if type(species) == dict:
                        species = [species]
                        
                        
                    for specie in species:
                        if "@AirQualityIndex" in specie:
                            dailyaqidata = [date, d['@LocalAuthorityName'], specie['@AirQualityIndex'], specie['@SpeciesDescription'], specie['@SpeciesCode'], sitename, sitecode, sitetype, lat, long]
                            ddata.append(dailyaqidata)

print(ddata)

FILEPATH = r"C:\Temp\daily_london_air_quality.csv"

with open(FILEPATH, "w", encoding = "UTF8", newline = "") as file:
    writer = csv.writer(file)
    writer.writerow(csvheaders)
    writer.writerows(ddata)                     
        


# In[14]:


import pandas as pd

dailyaqi = pd.read_csv(r"C:\Temp\daily_london_air_quality.csv", sep=',')
dailyaqi


# In[15]:


#data description
dailyaqi.dtypes


# In[16]:


dailyaqi.info()


# In[17]:


#change date to datetime type

dailyaqi['Date'] = pd.to_datetime(dailyaqi['Date'])


# In[18]:


# round up longitude and latitude columns 

dailyaqi['Latitude'] = dailyaqi['Latitude'].round(2)
dailyaqi['Longitude'] = dailyaqi['Longitude'].round(2)


# In[19]:


dailyaqi.dtypes


# In[20]:


dailyaqi.shape


# In[21]:


dailyaqi.describe()


# In[22]:


#clean data

#missing values 
print("missing vals (%) per field:\n", 100*dailyaqi.isnull().mean())


# In[23]:


#duplicate data 

#non-numeric cols 

non_numeric_cols = list(dailyaqi.select_dtypes(exclude=('int', 'float')).columns)

non_numeric_cols


# In[24]:


print("duplication overall: ", 100*(len(dailyaqi)-len(dailyaqi.drop_duplicates()))/len(dailyaqi),
      "%\nduplication in site name: ", 100*(len(dailyaqi["Site Name"])-len(dailyaqi["Site Name"].drop_duplicates()))/len(dailyaqi["Site Name"]), "%")

sites = dailyaqi['Site Name'].sort_values().unique()
#print(sites)


# In[177]:


dailyaqi = dailyaqi.drop_duplicates()
dailyaqi


# In[26]:


#data for Bexley 
dailyaqi.columns

bexdata = dailyaqi.loc[(dailyaqi['Site Name']=="Bexley - Belvedere West")]
bexdata


# In[42]:


import plotly as py 
import plotly.express as px 
import plotly.graph_objs as go

fig = px.bar(dailyaqi, x = "Pollutant", y = "AQI", color = "Authority Name", title = "Daily AQI for pollutants in sites around London")
fig.show()


# In[179]:


dailyaqi


# In[183]:


pollutantaqi = dailyaqi.pivot(columns = "Pollutant", values = "AQI").reset_index()
pollutantaqi


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[28]:


dailyaqi.head()


# In[29]:


dailyaqi.dtypes


# In[30]:


dailyaqi['Pollutant Description'].astype(str)


# In[31]:


smalldf = dailyaqi.drop(columns=["Pollutant Description"])
smalldf


# In[32]:


data2


# In[33]:


data2 = data2.rename(columns = {'Authority': 'Authority Name'})
data2.head()


# In[34]:


avgaqi=smalldf.groupby("Authority Name")["AQI"].mean().round(2).reset_index()
avgaqi


# In[99]:


geodf = pd.merge(data2, avgaqi)
geodf


# In[ ]:





# In[100]:


import geopandas as gpd
import matplotlib.pyplot as plt
f1 = r"C:\Users\Krupa\Downloads\statistical-gis-boundaries-london (1)\statistical-gis-boundaries-london\ESRI\London_Borough_Excluding_MHW.shp"
map_df = gpd.read_file(f1)
#1 = pd.read_csv(f1)
map_df.head()

#"C:\Users\Krupa\Downloads\statistical-gis-boundaries-london (1)\statistical-gis-boundaries-london\ESRI\London_Borough_Excluding_MHW.shp"


# In[149]:


map_df.to_crs(epsg=4326).plot(figsize=(15,8))
x= merged['Longitude']
y= merged['Latitude']
plt.scatter(x= x, y= y, c="black")
#authorities = [merged['NAME']]

#for authorityname in authorities:
   # print(authorityname)
 #   plt.text(x+.03,y+.03, authorityname, fontsize=10)
    


# In[101]:


geodf.plot(x="Longitude", y ="Latitude", kind = "scatter", c = "AQI", colormap = "Blues")


# In[103]:


#plt.plot(map_df)
map_df.plot()


# In[104]:


#join geo df with aqi df
merged = map_df.set_index("NAME").join(geodf.set_index("Authority Name")).reset_index()
merged


# In[112]:


#set variable to call a column to visualise on map 
variable = "AQI"

#set range for choropleth
vmin, vmax = 1, 10

#create fig
fig, ax = plt.subplots(1, figsize=(15,8))
merged.plot(column = variable, cmap = "Greens", linewidth = 0.8, ax = ax, edgecolor = "grey", missing_kwds = {'color':'lightgrey'})
#plt.scatter(x = merged['Longitude'], y =  merged['Latitude'], c = "black")


#formatting
#ax.axis("off")
ax.set_title("Daily AQI for London Boroughs, 18/06/23")
#ax.grid(b=True, alpha = 0.5)
 
#create a scale for AQI 
sm = plt.cm.ScalarMappable(cmap="Greens", norm=plt.Normalize(vmin=vmin, vmax=vmax))
# empty array for the data range
sm._A = []
# add the colorbar to the figure
cbar = fig.colorbar(sm)


# In[ ]:





# In[186]:





# In[ ]:





# In[ ]:





# In[ ]:




