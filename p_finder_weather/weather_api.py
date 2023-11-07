"""
Request weather data from https://open-meteo.com/ using its API https://open-meteo.com/en/docs/historical-weather-api 
    *Geodata from MeteoAPI about Merida, Yuacatan
        *Latitude: 20.97537
        *Longitude: -89.61696
        *Elevation: 14
        *Population: 777615
        *Admin1: Yucatán (Name of hierarchical administrative areas this location resides in. Admin1 is the first administrative level. Admin2 the second administrative level.)
        *Admin2: Mérida
        *Feature code: PPLA (Type of this location.)
"""
""" AQ variables
        *Particulate Matter PM10/Particulate Matter PM2.5: Particulate matter with diameter smaller than 10 µm (PM10) and smaller than 2.5 µm (PM2.5) close to surface (10 meter above ground)
        *Carbon Monoxide CO/Nitrogen Dioxide NO2/Sulphur Dioxide SO2/Ozone O3: Atmospheric gases close to surface (10 meter above ground)
        *Aerosol Optical Depth: Aerosol optical depth at 550 nm of the entire atmosphere to indicate haze
        *Dust: Saharan dust particles close to surface level (10 meter above ground).
        *UV Index/UV Index Clear Sky: UV index considering clouds and clear sky.
"""
""" WT variables
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

    SR variables   
        *shortwave_radiation_instant
        *direct_radiation_instant
        *diffuse_radiation_instant
"""
import requests

geo_coordinates = {
    "abala" : [20.63854,-89.65876],
    "acanceh" : [20.81321,-89.45286],
    "akil" : [20.26308,-89.34596],
    "baca" : [21.10857,-89.39913],
    "bokoba" : [21.01667,-89.18333],
    "buctzotz" : [21.20075,-88.79046],
    "cacalchen" : [20.51667,-88.76667],
    "calotmul" : [21.02165,-88.17625],
    "cansahcab" : [21.15790,-89.10223],
    "cantamayec" : [20.47073,-89.08119],
    "celestun" : [20.86667,-90.40000],
    "cenotillo" : [20.96853,-88.60060],
    "chacsinkin" : [20.93333,-89.66667],
    "chankom" : [20.56846,-88.51254],
    "chapab" : [20.45747,-89.45766],
    "chemax" : [20.65645,-87.93603],
    "chichimila" : [20.45942,-88.20996],
    "chicxulub-Pueblo" : [21.30000,-89.60000],
    "chikindzonot" : [20.33213,-88.48715],
    "chochola" : [21.16667,-88.11667],
    "chumayel" : [20.43263,-89.30156],
    "conkal" : [21.07499,-89.51942],
    "cuncunul" : [20.63939,-88.29785],
    "cuzama" : [20.71171,-89.32681],
    "dzan" : [20.38333,-89.46667],
    "dzemul" : [21.21037,-89.30935],
    "dzidzantun" : [21.20583,-88.97472],
    "dzilam-de-Bravo" : [21.39277,-88.89149],
    "dzilam-Gonzalez" : [21.22497,-88.92276],
    "dzitas" : [20.83891,-88.52843],
    "dzoncauich" : [21.05247,-88.89368],
    "espita" : [21.01296,-88.30667],
    "halacho" : [20.50614,-90.11199],
    "hocaba" : [20.81403,-89.24695],
    "hoctun" : [20.91236,-89.19634],
    "homun" : [20.73796,-89.28535],
    "huhi" : [21.28333,-89.25000],
    "hunucma" : [21.01814,-89.87534],
    "ixil" : [21.16667,-89.46667],
    "izamal" : [20.95190,-89.11825],
    "kanasin" : [20.93224,-89.55702],
    "kantunil" : [20.75649,-88.92948],
    "kaua" : [20.62195,-88.41431],
    "kinchil" : [20.87168,-90.08332],
    "Kopoma" : [20.62457,-89.89064],
    "mama" : [20.47755,-89.36474],
    "mani" : [20.38333,-89.40000],
    "maxcanu" : [20.58564,-90.00664],
    "mayapan" : [20.46743,-89.21413],
    "merida" : [21.04023,-89.56206],
    "mococha" : [20.35000,-88.30000],
    "motul" : [21.10024,-89.27753],
    "muna" : [19.90833,-89.50000],
    "muxupip" : [21.04293,-89.32970],
    "opichen" : [20.55009,-89.85738],
    "oxkutzcab" : [20.22723,-89.46737],
    "panaba" : [21.29630,-88.27028],
    "peto" : [20.12627,-88.92283],
    "quintana-roo" : [20.86789,-88.63165],
    "rio-lagartos" : [21.59644,-88.16449],
    "sacalum" : [20.49541,-89.59095],
    "samahil" : [20.88316,-89.88905],
    "sanahcat" : [20.77257,-89.21490],
    "santa-Elena" : [20.32784,-89.64407],
    "seye" : [20.87810,-89.32822],
    "sinanche" : [21.35242,-89.17177],
    "sotuta" : [20.59673,-89.00673],
    "sucila" : [21.15477,-88.31219],
    "sudzal" : [20.87059,-88.98893],
    "suma" : [21.10656,-89.15926],
    "tahdziu" : [20.32336,-88.84467],
    "tahmek" : [20.87537,-89.25557],
    "teabo" : [20.40033,-89.28545],
    "tecoh" : [20.69612,-89.39330],
    "tekal-de-Venegas" : [21.01346,-88.94708],
    "tekanto" : [21.01171,-89.10689],
    "tekax" : [19.87729,-89.21382],
    "tekit" : [20.53288,-89.33137],
    "tekom" : [20.54915,-88.41546],
    "telchac-Pueblo" : [21.23202,-89.27543],
    "telchac-Puerto" : [21.34210,-89.26246],
    "temax" : [21.13108,-88.98224],
    "temozon" : [20.80200,-88.20077],
    "tepakan" : [21.05000,-89.05000],
    "tetiz" : [20.97481,-89.96881],
    "teya" : [21.04907,-89.07410],
    "ticul" : [20.39849,-89.53791],
    "timucuy" : [21.20000,-89.00000],
    "tinum" : [20.78213,-88.41162],
    "tixcacalcupul" : [20.35836,-88.30267],
    "tixkokob" : [20.96549,-89.34880],
    "tixmehuac" : [20.53333,-90.00000],
    "tixpehual" : [21.00000,-89.46667],
    "tizimin" : [21.16150,-88.04736],
    "tunkas" : [20.90099,-88.75130],
    "tzucacab" : [20.07802,-89.14790],
    "uayma" : [21.11667,-88.90000],
    "ucu" : [21.03333,-89.75000],
    "uman" : [20.87999,-89.74698],
    "valladolid" : [20.68861,-88.19972],
    "xocchel" : [20.83324,-89.18334],
    "yaxcaba" : [20.52522,-88.73331],
    "yaxkukul" : [21.06243,-89.41909],
    "yobain" : [21.35650,-89.11732]

    # "caucel" : [21.015586, -89.702086],
    # "chuburna" : [21.262151, -89.819370],
    # "cholul" : [21.045995, -89.559671],
    # "progreso" : [21.283836, -89.673231],
    # "santa_clara" : [21.378090, -89.023122],
    # "sisal" : [21.171907, -90.034390]
}
# https://open-meteo.com/en/docs/air-quality-api#current=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,aerosol_optical_depth,dust,uv_index,uv_index_clear_sky&hourly=&timezone=GMT&forecast_days=1&domains=cams_global
current_aq = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=21.04023&longitude=-89.56206&current=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,aerosol_optical_depth,dust,uv_index,uv_index_clear_sky&timezone=GMT&forecast_days=1&domains=cams_global"
# https://open-meteo.com/en/docs#latitude=21.096545&longitude=-89.282273&current=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation,rain,showers,cloudcover,windspeed_10m,winddirection_10m,windgusts_10m&minutely_15=&hourly=shortwave_radiation_instant,direct_radiation_instant,diffuse_radiation_instant&timezone=GMT&forecast_days=1
current_wt_sr = "https://api.open-meteo.com/v1/forecast?latitude=21.096545&longitude=-89.282273&current=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation,rain,showers,cloudcover,windspeed_10m,winddirection_10m,windgusts_10m&hourly=shortwave_radiation_instant,direct_radiation_instant,diffuse_radiation_instant&timezone=GMT&forecast_days=1"

import pdb; pdb.set_trace()
weath_response = requests.get(meteo_url)
weath_data = weath_response.json()


