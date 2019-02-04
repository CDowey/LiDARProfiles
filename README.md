# LiDARProfiles
A series of scripts for constructing profiles from DEMs.

ProfileFunctions_arcpy.py uses the ArcGIS arcpy module for extracting elevation information along profile lines.

ProfileFunctions_rasterio.py completes the same task but with open-source tools such as rasterio and geopandas.

## Example Plots

An example from Mt. Ellen, Vermont comparing the [USGS 10m DEM](https://www.usgs.gov/core-science-systems/national-geospatial-program/national-map) against newly available [VCGI 0.7m LiDAR DEM](https://maps.vcgi.vermont.gov/arcgis/rest/services/EGC_services/IMG_VCGI_LIDARDEM_SP_NOCACHE_v1/ImageServer).

![MTELLEN](../master/MtEllen_10m_LiDAR.jpg)
