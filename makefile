# --- Environment variables for loading the elevation data ---

# Donwload base url
SRTM_URL=https://dds.cr.usgs.gov/srtm/version2_1/SRTM3/Eurasia/
# Minimal longitude for which area the data will be downloaded (must be of type integer)
MIN_LON=47
# Maximal longitude for which area the data will be downloaded (must be of type integer)
MAX_LON=55
# Minimal latitude for which area the data will be downloaded (must be of type integer)
MIN_LAT=6
# Maximal latitude for which area the data will be downloaded (must be of type integer)
MAX_LAT=15

# --- Environment variables for loading OSM data ---

# Donwload base url
OSM_URL=http://download.geofabrik.de/europe/germany/
# Donwload file name (without extension)
OSM_FILE=baden-wuerttemberg-latest

# --- Environment variables assigning the appropriate ports to the routing engine ---

# Port for the routing engine with the car profile
OSRM_CAR_PORT=5000
# Port for the routing engine with the electric car profile
OSRM_ELECTRIC_PORT=6000

# Internal use
DATA_FOLDER=data
RASTER_FOLDER=$(DATA_FOLDER)/raster
POSTGRES_PW=mysecretpassword

# Loads the elevation data from the internet (if not exist)
fetch-elevation: start-postgis
	@echo "Fetching elevation data..."
	@mkdir -p $(RASTER_FOLDER)
	@sh scripts/fetch-srtm.sh $(SRTM_URL) $(MIN_LON) $(MAX_LON) $(MIN_LAT) $(MAX_LAT) $(RASTER_FOLDER)

# Extracts the elevation data
extract-elevation: fetch-elevation
	@echo "Extracting elevation data..."
	@sh scripts/extract-srtm.sh $(RASTER_FOLDER)

# Starts the postgis docker container
start-postgis: 
	@echo "Starting postgis..."
	@sh scripts/startup-postgis.sh $(POSTGRES_PW) $(DATA_FOLDER)
	@sleep 30

# Loads the elevation data into the postgis docker container
load-postgis: extract-elevation
	@echo "Loading elevation data into Postgis..."
	@docker exec -it elevation_postgis bash \
		-c "raster2pgsql -s 4326 -t 50x50 -I -F $(RASTER_FOLDER)/*.hgt public.elevation_raster \
		| psql -d postgres -U postgres"

# Downloads the osm data
fetch-osm:
	@echo "Fetching osm map..."
	@mkdir -p osrm
	@sh scripts/fetch-osm.sh $(OSM_URL) $(OSM_FILE)

# starts the routing engine for the car profile
routing-car: start-postgis fetch-osm 
	@echo "Starting car routing engine..."
	@rm -rf osrm/car
	@mkdir -p osrm/car
	@cp osrm/$(OSM_FILE).osm.pbf profiles/car.lua osrm/car/
	@sh scripts/startup-routing.sh $(OSM_FILE) osrm car $(OSRM_CAR_PORT)

# starts the routing engine for the electric profile
routing-electric: load-postgis fetch-osm 
	@echo "Starting electric routing engine..."
	@rm -rf osrm/electric
	@mkdir -p osrm/electric
	@cp osrm/$(OSM_FILE).osm.pbf profiles/electric.lua osrm/electric/
	@sh scripts/startup-routing.sh $(OSM_FILE) osrm electric $(OSRM_ELECTRIC_PORT)

# starts both routing engines
start: routing-car routing-electric
	@echo "Routing engines are now up and running"