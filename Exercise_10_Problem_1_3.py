#!/usr/bin/env python
# coding: utf-8

# ## Problem 1: Geocode shopping centers
# 
# In problem 1 the task is to find out the addresses for a list of shopping centers and to geocode these addresses in order to represent them as points. The output should be stored in a Shapefile called `shopping_centers.shp` 
# 

# Import modules
import geopandas as gpd
import pandas as pd
# Read the data (replace "None" with your own code)
data = None
# YOUR CODE HERE 1 to read the data
data=pd.read_table('shopping_centers.txt', sep=';', header=None)
data.columns=['id','name', 'addr']
#TEST COEE
# Check your input data
print(data)

# - Geocode the addresses using the Nominatim geocoding service. Store the output in a variable called `geo`:

# Geocode the addresses using Nominatim
geo = None
from geopandas.tools import geocode

# Geocode addresses using Nominatim. Remember to provide a custom "application name" in the user_agent parameter!
#YOUR CODE HERE 2 for geocoding
geo = geocode(data['addr'], provider='nominatim', user_agent='autogis_xx')
#TEST CODE
# Check the geocoded output
print(geo)

#TEST CODE
# Check the data type (should be a GeoDataFrame!)
print(type(geo))


# Check that the coordinate reference system of the geocoded result is correctly defined, and **reproject the layer into JGD2011** (EPSG:6668):

# YOUR CODE HERE 3 to set crs.
geo = geo.to_crs(6668)
#TEST CODE
# Check layer crs
print(geo.crs)


# YOUR CODE HERE 4 to join the tables
geodata = None
geodata =geo.join(data)
#TEST CODE
# Check the join output
print(geodata.head())


# - Save the output as a Shapefile called `shopping_centers.shp` 

# Define output filepath
out_fp = None
# YOUR CODE HERE 5 to save the output
out_fp = r"shopping_centers.shp"
geodata.to_file(out_fp)
# TEST CODE
# Print info about output file
print("Geocoded output is stored in this file:", out_fp)


# ## Problem 2: Create buffers around shopping centers
# 
# Let's continue with our case study and calculate a 1.5 km buffer around the geocoded points. 


# YOUR CODE HERE 6 to create a new column
geodata['buffer']=None
# YOUR CODE HERE 7 to set buffer column
geodata = geodata.to_crs(32634)
geodata['buffer'] = geodata['geometry'].buffer(distance=1500)
#TEST CODE
print(geodata.head())

#TEST CODE
# Check the data type of the first value in the buffer-column
print(type(geodata.at[0,'buffer']))


#TEST CODE
# Check the areas of your buffers in km^2
print(round(gpd.GeoSeries(geodata["buffer"]).area / 1000000))


# - Replace the values in `geometry` column with the values of `buffer` column:

# YOUR CODE HERE 8 to replace the values in geometry
geodata['geometry'] =geodata['buffer']
#TEST CODE
print(geodata.head())


# ## Problem 3: How many people live near shopping centers? 
# 
# Last step in our analysis is to make a spatial join between our buffer layer and population data in order to find out **how many people live near each shopping center**. 
# 

# YOUR CODE HERE 9
pop=None
# Read population grid data for 2018 into a variable `pop`. 
pop=gpd.read_file(r"data/500m_mesh_suikei_2018_shape_13/500m_mesh_2018_13.shp")
pop = pop[["PTN_2020", "geometry"]]
geodata = geodata.to_crs(pop.crs)
print(pop.crs)
print(geodata.crs)
#TEST CODE
# Check your input data
print("Number of rows:", len(pop))
print(pop.head(3))


# In[ ]:


# Create a spatial join between grid layer and buffer layer. 
# YOUR CDOE HERE 10 for spatial join
join = gpd.sjoin(geodata, pop, how="inner", op="intersects")
tokyu = join.loc[join["name"] == "Tokyu Department Store"]
seibu = join.loc[join["name"] == "Seibu Shibuya Store"]
azabu = join.loc[join["name"] == 'National Azabu']


# YOUR CODE HERE 11 to report how many people live within 1.5 km distance from each shopping center
tokyu_sum=round(tokyu["PTN_2020"].sum())
seibu_sum=round(seibu["PTN_2020"].sum())
azabu_sum=round(azabu["PTN_2020"].sum())
# **Reflections:**
# 
# - How challenging did you find problems 1-3 (on scale to 1-5), and why?
# - What was easy?
# - What was difficult?

# YOUR ANSWER HERE
#Problem1 is 5
#Problem2 is 5
#Problem3 is 5
#It is very difficult for me to make an address.
#It was never easy
#To make an address
# Well done!
