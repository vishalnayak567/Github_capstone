
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import requests
import yaml
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import bokeh.models as bkm

business = pd.read_csv("F:/python/Capstone/Yelp csv files/csv files/yelp_business.csv")


# In[2]:


# to check null values in the business dataset
business.isnull().sum().sort_values(ascending = False)


# In[3]:


# to check if the business ID has unique values
business.business_id.is_unique


# In[9]:


def Top10business():
    # Top 10 cities with most number of business
    city_busi_counts = business[['city', 'business_id']].groupby(['city'])    ['business_id'].agg('count').sort_values(ascending=False)
    city_busi_counts = pd.DataFrame(data = city_busi_counts)
    city_busi_counts.rename(columns={'business_id' : 'No_of_businesses'}, inplace=True)

    city_busi_counts[0:10].sort_values(ascending=False, by="No_of_businesses")    .plot(kind='bar', stacked=False, figsize=[12,6])
    plt.title('Top 10 cities by businesses listed')


# In[10]:


Top10business()


# In[11]:


def top10cat():
    # What are the popular business categories?
    business_categ=' '.join(business['categories'])
    categ=pd.DataFrame(business_categ.split(';'),columns=['category'])
    x=categ.category.value_counts()
    print("There are ",len(x)," different types/categories of Businesses in Yelp!")
    #prep for chart
    x=x.sort_values(ascending=False)
    x=x.iloc[0:10]
    
    plt.figure(figsize=(12,8))
    ax = sns.barplot(x.index, x.values, alpha=0.8)
    plt.title("top10 categories",fontsize=25)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=75)
    plt.ylabel('# businesses', fontsize=12)
    plt.xlabel('Category', fontsize=12)


# In[12]:


top10cat()


# In[17]:


# Install mpl_toolkits in the terminal for swwing the geo visualization
import matplotlib.gridspec as gridspec
import matplotlib.gridspec as gridspec 

# graph viz
import plotly.offline as pyo
from plotly.graph_objs import *
import plotly.graph_objs as go

#map section
import imageio
import folium
import folium.plugins as plugins
from mpl_toolkits.basemap import Basemap


# In[18]:


def Geoview():
    #basic basemap of the world
    plt.figure(1, figsize=(15,6))
    # use ortho projection for the globe type version
    m1=Basemap(projection='ortho',lat_0=20,lon_0=-40)

    # hex codes from google maps color pallete = http://www.color-hex.com/color-palette/9261
    #add continents
    m1.fillcontinents(color='#bbdaa4',lake_color='#4a80f5') 
    # add the oceans
    m1.drawmapboundary(fill_color='#4a80f5')                
    # Draw the boundaries of the countires
    m1.drawcountries(linewidth=0.1, color="black")

    #Add the scatter points to indicate the locations of the businesses
    mxy = m1(business["longitude"].tolist(), business["latitude"].tolist())
    m1.scatter(mxy[0], mxy[1], s=3, c="red", lw=3, alpha=1, zorder=5)
    plt.title("World-wide Yelp Reviews")
    plt.show()


# In[19]:


Geoview()


# In[20]:


from bokeh.plotting import gmap, save
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook
import bokeh.palettes as palette
from bokeh.models import Range1d
output_notebook()


# In[24]:


def Yelpdash():
    from bokeh.io import output_file, output_notebook, show
    from bokeh.models import (
      GMapPlot, GMapOptions, ColumnDataSource, Circle, LogColorMapper, BasicTicker, ColorBar,
        DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, HoverTool
    )
    from bokeh.models.mappers import ColorMapper, LinearColorMapper
    from bokeh.palettes import Viridis5
    
    demo = business[(business.stars >= 4) & (business.review_count >= 100)]
    demo.head()

    map_options = GMapOptions(lat=32.7766, lng=-96.7969, map_type="roadmap", zoom=10)

    plot = GMapPlot(
        x_range=Range1d(start = 250, end = -250), y_range=Range1d(start = 90, end = -90), map_options=map_options,
        plot_width=1000, plot_height=600)
    plot.title.text = "Hey look! It's a scatter plot on a map!"

    # For GMaps to function, Google requires you obtain and enable an API key:
    #
    #     https://developers.google.com/maps/documentation/javascript/get-api-key
    #
    # Replace the value below with your personal API key:
    plot.api_key = "AIzaSyBYrbp34OohAHsX1cub8ZeHlMEFajv15fY"

    source = ColumnDataSource(
        data=dict(
            name= business.name,
            lat=demo.latitude,
            lon=demo.longitude,
            size=demo.stars,
            color=demo.review_count
        )
    )

    TOOLTIPS = [
        ("Business Name", "@name"),
        ("Star Rating:", "@size{(0.0)}"),
        ("Total reviews", "@color")
    ]

    color_mapper = LinearColorMapper(palette=Viridis5)

    circle = Circle(x="lon", y="lat", size="size", fill_color={'field': 'color', 'transform': color_mapper}, fill_alpha=0.5, line_color=None)
    plot.add_glyph(source, circle)

    color_bar = ColorBar(color_mapper=color_mapper, ticker=BasicTicker(),
                         label_standoff=12, border_line_color=None, location=(0,0))
    plot.add_layout(color_bar, 'right')

    plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool(),  HoverTool(tooltips=TOOLTIPS))
    ##output_file("gmap_plot.html")
    #output_notebook()

    show(plot)


# In[25]:


Yelpdash()

