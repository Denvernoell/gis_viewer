#%%
# from pyperclip import copy
# '/c/Users/Denver/AppData/Local/pypoetry/Cache/virtualenvs/geoedit-1JcP-oDe-py3.10/Scripts/python.exe -m streamlit run wq_stream.py'
#%%
#%%
import streamlit as st
from pathlib import Path
import matplotlib.pyplot as plt
import geopandas as gpd
import fiona
import contextily as cx

# '/c/Users/Denver/AppData/Local/pypoetry/Cache/virtualenvs/stream-cRD5AfwB-py3.10/Scripts/python.exe -m streamlit run wq_stream.py'



# """Current Database from Cheryl"""

# base_path = r'\\ppeng.com\pzdata\clients\Aliso WD-2500\Ongoing\GIS'
# base_path = r'\\ppeng.com\pzdata\clients\Tranquillity ID-1075\Ongoing-1075'
base_path = st.text_input('Folder')

"""Shapefiles"""
# get_relative = lambda L: [i.relative_to(base_path) for i in L]
get_relative = lambda i: i.relative_to(base_path)

shapefiles = {get_relative(i):i for i in Path(base_path).glob('**/*.shp')}
gdbs = {get_relative(i):i for i in Path(base_path).glob('**/*.gdb')}


file_type = st.selectbox('File Type',['Shapefiles','Geodatabases'])


if file_type == 'Geodatabases':
	file = st.selectbox('File',gdbs.keys())
	file_path = gdbs[file]

	gdb = {i:gpd.read_file(file_path,layer=i) for i in fiona.listlayers(file_path)}
	layers = [i for i in gdb.keys()]
	layer = st.selectbox('Layer',layers)
	gdf = gdb[layer]

else:
	file = st.selectbox('File',shapefiles.keys())
	file_path = shapefiles[file]
	gdf = gpd.read_file(file_path)


fig,ax = plt.subplots(1,1,figsize=(10,10))

# Plot all sections
splot = gdf.plot(
	ax=ax,
	# edgecolor='black',
	figsize=(10,10)
	)


# base_plot = gdf.plot(
# 	# ax=ax,
# 	# edgecolor='black',
# 	figsize=(10,10)
# 	)

# ax1 = parcel.plot(ax=splot,column='Section')
# # parcel.plot(ax=splot,column='Section',categorical=True)
# # parcel.plot(ax=ax2,column='Section',legend=True,legend_kwds={'fmt':'{:.0f}'},categorical=True)
# parcel.plot(ax=ax2,column='Section',legend=True,categorical=True,legend_kwds={'bbox_to_anchor':(.5,0.5)})

# """Plot"""
# cx.add_basemap(base_plot,source=cx.providers.Stamen.TonerLite)

st.pyplot(fig)

# st.map(gdf)
# st.write(gdf.explore())

st.markdown(f"Size = {gdf.shape}")
# st.markdown(columns)
columns = [i for i in gdf.columns]
columns.remove('geometry')
s_columns = st.multiselect('columns',columns,default=columns)
# st.dataframe(gdf.describe())


# st.write(gdf)
# st.dataframe(gdf.loc[:,gdf.columns != 'geometry' ])
st.dataframe(gdf[s_columns])
