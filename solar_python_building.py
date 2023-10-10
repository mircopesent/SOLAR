import processing
from bs4 import BeautifulSoup
import numpy as np

months=[31,28,31,30,31,30,31,31,30,31,30,31]

month_span=[2,4,6,8,10,12]
day_span=[7,23]


for i in month_span:

    for j in day_span:
            file_name_clipped='C:/Users/mirco/Documents/EPFL/MA3/solar_energy_conversion/exercices/GHI_clipped/msg.SIS.D_ch02.lonlat_2014'+str(i).zfill(2)+str(j).zfill(2) +'000000_clipped.tif'
            file_name_clipped_building='C:/Users/mirco/Documents/EPFL/MA3/solar_energy_conversion/exercices/GHI_clipped_building/msg.SIS.D_ch02.lonlat_2014'+str(i).zfill(2)+str(j).zfill(2) +'000000_clipped_building.tif'
            file_name_vector_layer_building='C:/Users/mirco/Documents/EPFL/MA3/solar_energy_conversion/exercices/GHI_vector_layer_building/msg.SIS.D_ch02.lonlat_2014'+str(i).zfill(2)+str(j).zfill(2) +'000000_vector_layer_building.tif'
            file_name_vector_final_building='C:/Users/mirco/Documents/EPFL/MA3/solar_energy_conversion/exercices/GHI_vector_final_building/msg.SIS.D_ch02.lonlat_2014'+str(i).zfill(2)+str(j).zfill(2) +'000000_vector_final_building.gpkg'
            file_name_vector_area_building='C:/Users/mirco/Documents/EPFL/MA3/solar_energy_conversion/exercices/GHI_vector_area_building/msg.SIS.D_ch02.lonlat_2014'+str(i).zfill(2)+str(j).zfill(2) +'000000_vector_area_building.gpkg'
            file_name_output_building='C:/Users/mirco/Documents/EPFL/MA3/solar_energy_conversion/exercices/data_building/data_building'+str(i).zfill(2)+str(j).zfill(2)+'.csv'
            file_name_html_building='C:/Users/mirco/Documents/EPFL/MA3/solar_energy_conversion/exercices/max_values_building/stats_building_2014'+str(i).zfill(2)+str(j).zfill(2) +'000000_.html'

            processing.run("gdal:cliprasterbymasklayer", {'INPUT':file_name_clipped,'MASK':'C:/Users/mirco/Documents/EPFL/MA3/solar_energy_conversion/exercices/swissTLMRegio_Product_LV95.gdb|layername=TLMRegio_Building','SOURCE_CRS':None,'TARGET_CRS':None,'TARGET_EXTENT':None,'NODATA':None,'ALPHA_BAND':False,'CROP_TO_CUTLINE':True,'KEEP_RESOLUTION':False,'SET_RESOLUTION':False,'X_RESOLUTION':None,'Y_RESOLUTION':None,'MULTITHREADING':False,'OPTIONS':'','DATA_TYPE':0,'EXTRA':'','OUTPUT':file_name_clipped_building})
            processing.run("native:rasterlayerstatistics", {'INPUT':file_name_clipped_building,'BAND':1,'OUTPUT_HTML_FILE':file_name_html_building})

            HTMLFileToBeOpened = open(file_name_html_building, "r")
            # Reading the file and storing in a variable
            contents = HTMLFileToBeOpened.read()
            beautifulSoupText = BeautifulSoup(contents, 'lxml')
            h=beautifulSoupText.text.split()
            max=float(h[h.index('maximale:')+1])
            if (max<0): max=0
            max_rounded=int(10*np.ceil(max/10))
            table_class=['0','10','5']
            for j in np.arange(10,max_rounded,10):
                table_class.append(str(j))
                table_class.append(str(j+10))
                table_class.append(str(j+5))
            processing.run("native:reclassifybytable", {'INPUT_RASTER':file_name_clipped_building,'RASTER_BAND':1,'TABLE':table_class,'NO_DATA':-9999,'RANGE_BOUNDARIES':0,'NODATA_FOR_MISSING':False,'DATA_TYPE':5,'OUTPUT':file_name_vector_layer_building})
            processing.run("gdal:polygonize", {'INPUT':file_name_vector_layer_building,'BAND':1,'FIELD':'DN','EIGHT_CONNECTEDNESS':False,'EXTRA':'','OUTPUT':file_name_vector_final_building})
            processing.run("native:fieldcalculator", {'INPUT':file_name_vector_final_building,'FIELD_NAME':'area','FIELD_TYPE':0,'FIELD_LENGTH':0,'FIELD_PRECISION':0,'FORMULA':'$area','OUTPUT':file_name_vector_area_building})
            processing.run("native:savefeatures", {'INPUT':file_name_vector_area_building,'OUTPUT':file_name_output_building,'LAYER_NAME':'','DATASOURCE_OPTIONS':'','LAYER_OPTIONS':''})