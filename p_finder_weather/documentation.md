# data from Open Meteo API 
The wesite is https://open-meteo.com/ we are going to use the API https://open-meteo.com/en/docs/historical-weather-api 
## Data about Merida, Yuacatan
        *Latitude: 20.97537
        *Longitude: -89.61696
        *Elevation: 14
        *Population: 777615
        *Admin1: Yucatán (Name of hierarchical administrative areas this location resides in. Admin1 is the first administrative level. Admin2 the second administrative level.)
        *Admin2: Mérida
        *Feature code: PPLA (Type of this location.)
## Considerations to use this API
10000 request per day for free

## Air quality and sun radiation variables to fetch from Meteo source
        *Particulate Matter PM10/Particulate Matter PM2.5: Particulate matter with diameter smaller than 10 µm (PM10) and smaller than 2.5 µm (PM2.5) close to surface (10 meter above ground)
        *Carbon Monoxide CO/Nitrogen Dioxide NO2/Sulphur Dioxide SO2/Ozone O3: Atmospheric gases close to surface (10 meter above ground)
        *Aerosol Optical Depth: Aerosol optical depth at 550 nm of the entire atmosphere to indicate haze
        *Dust: Saharan dust particles close to surface level (10 meter above ground).
        *UV Index/UV Index Clear Sky: UV index considering clouds and clear sky.

## WT variables to fetch from Meteo source
        *temperature_2m: Air temperature at 2 meters above ground
        *relativehumidity_2m: Relative humidity at 2 meters above ground
        *apparent_temperature	Instant	°C (°F)	Apparent temperature is the perceived feels-like temperature combining wind chill factor, relative humidity and solar radiation
        *precipitation: Total precipitation (rain, showers, snow) sum of the preceding hour
        *rain: Rain from large scale weather systems of the preceding hour in millimeter
        *showers: Showers from convective precipitation in millimeters from the preceding hour{}
        *cloudcover
        *windspeed_10m
        *winddirection_10m
        *windgusts_10

### Extra information SR variables   
        *shortwave_radiation_instant
        *direct_radiation_instant
        *diffuse_radiation_instant
### Examples to query the API
current_aq = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=21.04023&longitude=-89.56206&current=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,aerosol_optical_depth,dust,uv_index,uv_index_clear_sky&timezone=GMT&forecast_days=1&domains=cams_global"
current_wt_sr = "https://api.open-meteo.com/v1/forecast?latitude=21.096545&longitude=-89.282273&current=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation,rain,showers,cloudcover,windspeed_10m,winddirection_10m,windgusts_10m&hourly=shortwave_radiation_instant,direct_radiation_instant,diffuse_radiation_instant&timezone=GMT&forecast_days=1"


# Geo coordinates of municipios and cities
We fetch geo-coordiantes of locality centroids from https://www.coordenadas.com.es/mexico/index.php
## Extra mucipalities
        {       
                "Quintana-Roo":{
                        Cozumel
                	Felipe Carrillo Puerto
                	Isla Mujeres
                	Othón P. Blanco	
                	Benito Juárez	
                	José María Morelos
                	Lázaro Cárdenas
                	Solidaridad	
                	Tulum
                	Bacalar
                	Puerto Morelos
                }
                "Yucatan":{
                        "caucel" : [21.015586, -89.702086],
                        "chuburna" : [21.262151, -89.819370],
                        "cholul" : [21.045995, -89.559671],
                        "progreso" : [21.283836, -89.673231],
                        "santa_clara" : [21.378090, -89.023122],
                        "sisal" : [21.171907, -90.034390]
                }
        }
