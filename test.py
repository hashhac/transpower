import json
import matplotlib.pyplot as plt
from gemini.regex_extraction import convert_cords
import pandas as pd
from typing import List, Tuple
with open('data/locations.json', 'r') as file:
    data_locations = json.load(file)

with open("data/nz_power_stations.json", 'r') as file:
    data_powerpalnts = json.load(file)

def remake_cords(data_powerpalnts : dict, key: str) -> List[Tuple[float,float]]:
    return [convert_cords(data["Coordinates"])  for data in data_powerpalnts[key]]

hydro_plants = remake_cords(data_powerpalnts,"Hydroelectric")
Wind_plants = remake_cords(data_powerpalnts,'Wind')
bioenenergy_plants =  remake_cords(data_powerpalnts,'bioenenergy')
Geothermal = remake_cords(data_powerpalnts,'Geothermal')
Fossil_fuel = remake_cords(data_powerpalnts,'Fossil-fuel-thermal')
Solar = remake_cords(data_powerpalnts,'Solar')
# because diferent proccessing the directions hasnt been applied but there are all in the same quadrent
locations = [(-1.0*item["latitude"],item["longitude"]) for item in data_locations]

power_data = {
    "All Locations": locations,
    "Hydro": hydro_plants,
    "Wind": Wind_plants,
    "Bioenergy": bioenenergy_plants,
    "Geothermal": Geothermal,
    "Fossil Fuel": Fossil_fuel,
    "Solar": Solar

}

colors = ["black","blue","green","red","cyan","magenta","yellow"]

plt.xlim(166, 179) # X is Longitude
plt.ylim(-48, -34) # Y is Latitude
axes = plt.gca()
axes.set_aspect('equal', adjustable='box')
rows = []
for (label, points), color in zip(power_data.items(), colors):
    # print(f"Label : {label}\nPoints : {points}\nColor : {color}")
    for point in points:
        if isinstance(point, tuple) and len(point) == 2:
            rows.append({
                    "Category": label,
                    "Lat": point[0],
                    "Lon": point[1],
                    "color":color
                })
            
    clean_points = [p for p in points if isinstance(p, tuple) and len(p) == 2]
    y_data, x_data = zip(*clean_points)
    
    # print(len(y_data))
    axes.scatter(x_data, y_data, c=color, label=label, s=30, alpha=0.7)
df = pd.DataFrame(rows)
print(df.head())
print(df[df.color=="yellow"])
plt.savefig('test.png')





