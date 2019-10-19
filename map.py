import folium
import pandas

#--------------------------------------------------------------------------

data = pandas.read_csv("Volcanoes.txt") # read data from file
lat = list(data["LAT"]) # get LAT column values and convert to list
lon = list(data["LON"]) # get LON column values and convert to list
elev = list(data["ELEV"]) # get ELEV column values and convert to list

#--------------------------------------------------------------------------

def color_producer(elevation):
    """ To get correct colour according to elevation values"""
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

#--------------------------------------------------------------------------

map = folium.Map(location=[38.58,-99.09], zoom_start=6, tiles="Stamen Terrain")

#--------------------------------------------------------------------------

fgv = folium.FeatureGroup(name="Volcanoes") # create feature group for volcanoes

# to create marker layer of volcanoes differenciate with colours
# [display green if less than 1000m, orange if greater than 1000m and less than 3000m
# else red clour will display].
for lt, ln, el in zip(lat, lon, elev): # using zip function to iterate values e.g. zip([1,2,3], [4,5,6]) output: [1,4],[2,5] .....
    
    # for normal marker
    # fg.add_child(folium.Marker(location=[lt,ln], popup=str(el)+" m", icon=folium.Icon(color=color_producer(el))))
    
    # for circle marker
    fgv.add_child(folium.CircleMarker(location=[lt,ln], popup=str(el)+" m", radius=8,
    fill_color=color_producer(el), color = 'grey', fill_opacity=0.5))

#-----------------------------------------------------------------------------

fgp = folium.FeatureGroup(name="Population") # create feature group for population

# to create polygon layer of population diffrenciate with colours 
# [display green if less than 10bn, orange if greater than 10bn and less than 20bn
# else red clour will display].
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), 
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

#-------------------------------------------------------------------------------

map.add_child(fgv) # for volcanoes
map.add_child(fgp) # for population

map.add_child(folium.LayerControl()) # to control layers

map.save("Map.html") # create html file with javascript and css to display on webpage.