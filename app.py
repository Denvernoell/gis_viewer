#%%
# from pyperclip import copy
# '/c/Users/Denver/AppData/Local/pypoetry/Cache/virtualenvs/geoedit-1JcP-oDe-py3.10/Scripts/python.exe -m streamlit run app.py'
#%%
#%%
import streamlit as st
from pathlib import Path
import matplotlib.pyplot as plt
import geopandas as gpd
import fiona
import contextily as cx




# """Current Database from Cheryl"""

# base_path = r'\\ppeng.com\pzdata\clients\Aliso WD-250	0\Ongoing\GIS'
# base_path = r'\\ppeng.com\pzdata\clients\Tranquillity ID-1075\Ongoing-1075'
# base_path = r'\\ppeng.com\pzdata\clients\Eastside WD-2344\234422001- Upland Pipeline Due Diligence\400 GIS'
base_path = st.text_input('Folder')

"""Shapefiles"""
# get_relative = lambda L: [i.relative_to(base_path) for i in L]
get_relative = lambda i: i.relative_to(base_path)

# @st.cache()
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

# gdf = gdf.to_crs(epsg='6420')
# st.markdown(gdf.crs)

fig,ax = plt.subplots(1,1,figsize=(10,10))


columns = [i for i in gdf.columns]
columns.remove('geometry')
s_columns = st.multiselect('columns',columns,default=columns)
column_color = st.selectbox('Color by',columns)
# Plot all sections


st.markdown(f"crs = {gdf.crs}")
# st.markdown(f"crs = {gdf.}")

# """Point"""
try:
	splot = gdf.plot(
	ax=ax,
	figsize=(10,10),
	column=column_color,
	legend=True,
	# cax=cax
	legend_kwds={
		'title':column_color,
		'bbox_to_anchor':(1,1)
		}
	
	)



except:
	"""Colorbar"""
	splot = gdf.plot(
	ax=ax,
	figsize=(10,10),
	column=column_color,
	legend=True,
	# cax=cax
	legend_kwds={
		}
	
	)

# remove axis
ax.set_axis_off()




# """Plot"""
cx.add_basemap(
	splot,
	# source=cx.providers.Stamen.TonerLite
	crs=gdf.crs,
	source=cx.providers.OpenStreetMap.Mapnik,
	)

st.pyplot(fig)

# st.map(gdf)
# st.write(gdf.explore())

st.markdown(f"Size = {gdf.shape}")
# st.markdown(columns)
# st.dataframe(gdf.describe())


# st.write(gdf)
# st.dataframe(gdf.loc[:,gdf.columns != 'geometry' ])
txt = ""
for i in s_columns:
	txt += f"- {i}"
	txt +='\n'

st.markdown(txt)
# if st.button('columns'):
# 	st.markdown('\n- '.join(s_columns))
st.dataframe(gdf[s_columns])

# %%
