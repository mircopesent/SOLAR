#Test QGIS Script
import os
import shutil

script_dir =os.path.expanduser('~/Documents/GitHub/solar_group_3/').replace('\\','/')

temp_dir = os.path.join(script_dir, 'Temp')
output_dir = os.path.join(script_dir, 'Output')

if (os.path.isdir(temp_dir)):
    shutil.rmtree(temp_dir)
os.makedirs(temp_dir)

if (os.path.isdir(output_dir)):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

#PATH_IN = os.path.join(script_dir)

boundaries = os.path.join(script_dir,'Data/swissBOUNDARIES3D_1_3_LV95_LN02.gdb|layername=TLM_LANDESGEBIET')

months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

day_counter = 1  # Initialize the day counter

# Define the maximum value
max_value = 1000
# Initialize the array with the initial values
table = [0, 10, 5]
# Determine the interval
interval = 10
# Extrapolate the array up to the maximum value
while int(table[-3]) < max_value-interval:
    table.append(table[-2])
    table.append(table[-1]+ interval)
    table.append(table[-3]+ interval)


for month, month_days in enumerate(months, start=1):
    for day_in_month in range(1, month_days + 1):
        day_counter += 1   

        fname_DNI = os.path.join(script_dir, f'Data/MSG_SIS_D_14/msg.SIS.D_ch02.lonlat_2014{month:02d}{day_in_month:02d}000000.nc')
        fname_GHI = os.path.join(script_dir, f'Data/MSG_SISDIR_D_14/msg.SISDIR.D_ch02.lonlat_2014{month:02d}{day_in_month:02d}000000.nc')
        
        raster = QgsRasterLayer(fname_GHI, "raster")

        stats = raster.dataProvider().bandStatistics(1, QgsRasterBandStats.All, raster.extent(), 0)
        
        max_value = stats.maximumValue
        
        #Import raster and clip it using Swiss boundaries
        mask_parameters = {'INPUT':fname_DNI,
                            'MASK':boundaries,
                            'SOURCE_CRS':None,
                            'TARGET_CRS':None,
                            'TARGET_EXTENT':None,
                            'NODATA':None,
                            'ALPHA_BAND':False,
                            'CROP_TO_CUTLINE':True,
                            'KEEP_RESOLUTION':False,
                            'SET_RESOLUTION':False,
                            'X_RESOLUTION':None,
                            'Y_RESOLUTION':None,
                            'MULTITHREADING':False,
                            'OPTIONS':'',
                            'DATA_TYPE':0,
                            'EXTRA':'',
                            'OVERWRITE': True,
                            'OUTPUT': temp_dir+ '/clipped_vector.tif'}
        processing.run("gdal:cliprasterbymasklayer", mask_parameters)

        #Reclassify clipped vector

        reclassify_parameters = {'INPUT_RASTER':temp_dir + '/clipped_vector.tif',
                                'RASTER_BAND':1,
                                'TABLE':table,
                                'NO_DATA':-9999,
                                'RANGE_BOUNDARIES':0,
                                'NODATA_FOR_MISSING':False,
                                'DATA_TYPE':5,
                                'OVERWRITE': True,
                                'OUTPUT':temp_dir+ '/reclassified_vector.tif'}
        processing.run("native:reclassifybytable", reclassify_parameters)

        #Polygonize reclassified vector
        polygonize_parameters = {'INPUT':temp_dir+ '/reclassified_vector.tif',
                                'BAND':1,
                                'FIELD':'DN',
                                'EIGHT_CONNECTEDNESS':False,
                                'EXTRA':'',
                                'OVERWRITE': True,
                                'OUTPUT':temp_dir+ '/polygonized_vector.gpkg'}
        processing.run("gdal:polygonize", polygonize_parameters)

        #Extract field parameters
        field_parameters = {'INPUT':temp_dir+ '/polygonized_vector.gpkg',
                            'FIELD_NAME':'area',
                            'FIELD_TYPE':0,
                            'FIELD_LENGTH':0,
                            'FIELD_PRECISION':0,
                            'FORMULA':'$area',
                            'OUTPUT':temp_dir+ f'/vector_area{month:02d}{day_in_month:02d}.gpkg',
                            'OVERWRITE': True,
                            'FORCE':True}
        processing.run("native:fieldcalculator", field_parameters)

        #Save features
        features_parameters = {'INPUT':temp_dir+ f'/vector_area{month:02d}{day_in_month:02d}.gpkg',
                            'OUTPUT':output_dir + f'/vector_features2014{month:02d}{day_in_month:02d}.csv',
                            'LAYER_NAME':'',
                            'DATASOURCE_OPTIONS':'',
                            'LAYER_OPTIONS':'',
                            'FORCE':True}
        processing.run("native:savefeatures", features_parameters)
    print(f"{month*100/12:.2f}%", end="\r")