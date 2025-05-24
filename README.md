# U.S. Census Tract Level Choropleth Map in Python: Highly Granular Geospatial Visualization
A full pipeline for creating highly granular, interactive choropleth maps of U.S. Census Tracts using public data and modern geospatial visualization tools. ~84,414 polygons.

**By [Jake Dugan](https://www.linkedin.com/in/jakedugan/)**  
**Companion blog post**: [How to Make a Census Tract Level Choropleth in Python](https://medium.com/@jakedugi/how-to-make-a-census-tract-level-choropleth-in-python-35ef0c8cae0e)

---

## Sample Output

![image](https://github.com/user-attachments/assets/cf8830da-49bf-44b2-a621-ea2a0b6d573f)


---

## Overview

Census tracts are small, relatively permanent subdivisions of counties with standard populations (~4,000 people). Unlike ZIP codes, they cover the entire U.S. and are ideal for fine-grained demographic or socioeconomic analysis.

This project demonstrates how to:
- Combine TIGER/Line shapefiles into a unified GeoJSON
- Clean and join ACS data at the tract level
- Render an interactive Plotly choropleth map using Mapbox
- Output a ready-to-share HTML visualization

**Data Sources**:
- [U.S. Census Bureau TIGER/Line® Shapefiles](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)
- [American Community Survey (ACS)](https://data.census.gov/)

_For theory, visuals, and simplification tradeoffs, [read the blog post](https://medium.com/@jakedugi/how-to-make-a-census-tract-level-choropleth-in-python-35ef0c8cae0e)._

---

## Features

-  GeoJSON simplification for tract-level mapping
-  Integrated ACS demographic data
-  Interactive and customizable choropleth rendering with Plotly & Mapbox
-  Modular Python structure with full pipeline orchestration

---

##  Project Structure
- `data/` – Raw input data
  - `tractzips/` – Unzipped shapefiles (.shp, .dbf, etc.)
  - `ACSST5Y2021.S2701-Data.csv` – Raw Census CSV
- `output/` – All outputs (not version-controlled)
  - `Blog_Data.csv` – Cleaned data
  - `Blog_Data_Processed.csv` – Final data for choropleth
  - `tracts1.geojson` – Combined tract-level polygons
  - `blog_tracts_zip.json` – Simplified GeoJSON via Mapshaper
  - `Blog_choropleth_map_FINAL.html` – Interactive HTML map
- `config/` – Configuration files
  - `accesstoken.txt` – Mapbox access token (excluded in `.gitignore`)
- `geojson_utils.py` – GeoJSON creation from shapefiles
- `data_processing.py` – CSV cleaning and transformation logic
- `visualization.py` – Plotly choropleth generation
- `config.py` – Directory and file path config
- `main.py` – End-to-end pipeline runner
- `requirements.txt` – Python dependencies
- `README.md` – Project overview and instructions
---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```
### 2. Add your Mapbox token
Save your [Mapbox access token](https://account.mapbox.com/access-tokens/) to:
```bash
config/accesstoken.txt
```
### 3. Run the pipeline
```bash
python main.py
```
This will:
* Merge shapefiles into a GeoJSON
* Clean and transform ACS data
* Output: output/Blog_choropleth_map_FINAL.html

 ---

## Customization Ideas
- Swap the ACS column (e.g., income, education, insurance rate)
- Simplify GeoJSON using [Mapshaper.org](https://mapshaper.org/)
- Add filters for regional analysis (e.g., zoom into California)
