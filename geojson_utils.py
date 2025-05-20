def convert_to_geojson(directory, output_path):
    shp_files = [file for file in os.listdir(directory) if file.endswith('.shp')]
    if shp_files:
        gdf_list = []
        for shp_file in shp_files:
            shp_path = os.path.join(directory, shp_file)
            try:
                gdf = gpd.read_file(shp_path)
                gdf['geometry'] = gdf['geometry'].apply(lambda geom: geom.buffer(0) if not geom.is_valid else geom)
                gdf_list.append(gdf)
            except Exception as e:
                print(f"Error reading {shp_path}: {e}")
        combined_gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
        combined_gdf.to_file(output_path, driver="GeoJSON")
        return output_path
    return None