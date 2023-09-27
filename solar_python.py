"""
Double-click on the history item or paste the command below to re-run the algorithm
"""

import processing
from bs4 import BeautifulSoup
import numpy as np

months=[31,28,31,30,31,30,31,31,30,31,30,31]


for i in range(1,13):

    for j in range(1,months[i-1]+1):
            file_name='C:/Users/mirco/Documents/EPFL/MA3/solar_energy_conversion/exercices/GHI-2014 Switzerland/MSG_SIS_D_14/msg.SIS.D_ch02.lonlat_2014'+str(i).zfill(2)+str(j).zfill(2) +'000000.nc'
            file_name_clipped='C:/Users/mirco/Documents/EPFL/MA3/solar_energy_conversion/exercices/GHI_clipped/msg.SIS.D_ch02.lonlat_2014'+str(i).zfill(2)+str(j).zfill(2) +'000000_clipped.tif'
            file_name_vector_layer='C:/Users/mirco/Documents/EPFL/MA3/solar_energy_conversion/exercices/GHI_vector_layer/msg.SIS.D_ch02.lonlat_2014'+str(i).zfill(2)+str(j).zfill(2) +'000000_vector_layer.tif'
            file_name_vector_final='C:/Users/mirco/Documents/EPFL/MA3/solar_energy_conversion/exercices/GHI_vector_final/msg.SIS.D_ch02.lonlat_2014'+str(i).zfill(2)+str(j).zfill(2) +'000000_vector_final.gpkg'
            file_name_vector_area='C:/Users/mirco/Documents/EPFL/MA3/solar_energy_conversion/exercices/GHI_vector_area/msg.SIS.D_ch02.lonlat_2014'+str(i).zfill(2)+str(j).zfill(2) +'000000_vector_area.gpkg'
            file_name_output='C:/Users/mirco/Documents/EPFL/MA3/solar_energy_conversion/exercices/data/data'+str(i).zfill(2)+str(j).zfill(2)+'.csv'
            file_name_html='C:/Users/mirco/Documents/EPFL/MA3/solar_energy_conversion/exercices/max_values/stats_2014'+str(i).zfill(2)+str(j).zfill(2) +'000000_.html'
            processing.run("gdal:cliprasterbymasklayer", {'INPUT':file_name,'MASK':'C:/Users/mirco/Documents/EPFL/MA3/solar_energy_conversion/exercices/Swiss_boundaries/swissBOUNDARIES3D_1_3_LV95_LN02.gdb|layername=TLM_LANDESGEBIET','SOURCE_CRS':None,'TARGET_CRS':None,'TARGET_EXTENT':None,'NODATA':None,'ALPHA_BAND':False,'CROP_TO_CUTLINE':True,'KEEP_RESOLUTION':False,'SET_RESOLUTION':False,'X_RESOLUTION':None,'Y_RESOLUTION':None,'MULTITHREADING':False,'OPTIONS':'','DATA_TYPE':0,'EXTRA':'','OUTPUT':file_name_clipped})
            processing.run("native:rasterlayerstatistics", {'INPUT':file_name_clipped,'BAND':1,'OUTPUT_HTML_FILE':file_name_html})

            HTMLFileToBeOpened = open(file_name_html, "r")
            # Reading the file and storing in a variable
            contents = HTMLFileToBeOpened.read()
            beautifulSoupText = BeautifulSoup(contents, 'lxml')
            h=beautifulSoupText.text.split()
            max=float(h[h.index('maximale:')+1])
            max_rounded=int(10*np.ceil(max/10))
            table_class=['0','10','5']
            for j in np.arange(10,max_rounded,10):
                table_class.append(str(j))
                table_class.append(str(j+10))
                table_class.append(str(j+5))
            processing.run("native:reclassifybytable", {'INPUT_RASTER':file_name_clipped,'RASTER_BAND':1,'TABLE':table_class,'NO_DATA':-9999,'RANGE_BOUNDARIES':0,'NODATA_FOR_MISSING':False,'DATA_TYPE':5,'OUTPUT':file_name_vector_layer})
            processing.run("gdal:polygonize", {'INPUT':file_name_vector_layer,'BAND':1,'FIELD':'DN','EIGHT_CONNECTEDNESS':False,'EXTRA':'','OUTPUT':file_name_vector_final})
            processing.run("native:fieldcalculator", {'INPUT':file_name_vector_final,'FIELD_NAME':'area','FIELD_TYPE':0,'FIELD_LENGTH':0,'FIELD_PRECISION':0,'FORMULA':'$area','OUTPUT':file_name_vector_area})
            processing.run("native:savefeatures", {'INPUT':file_name_vector_area,'OUTPUT':file_name_output,'LAYER_NAME':'','DATASOURCE_OPTIONS':'','LAYER_OPTIONS':''})
            