import json
import matplotlib.pyplot as plt
from gemini.regex_extraction import convert_cords
import pandas as pd
from typing import List, Tuple, Dict



def sort_string_to_NONE(data_string : str) -> any:
    try:
        if (len(data_string.split(','))) >= 2:
            data_string = data_string.split(',')[0]
        if (len(data_string.split('['))) >= 2:
            data_string  = data_string.split('[')[0]
        return float(data_string)
    except ValueError: 
        # print(f"Failed to conver another \n{'':_^80}\n Could not convert : {data_string} : SMH xP ;( \n{'':_^80}\n")
        return None

def remake_cords(data_powerpalnts : dict, key: str) -> list[dict[str, str | float]]:
    stuff = []
    for data in data_powerpalnts[key]:
        # TODO If there was more time i would use classses to do thiS!!!! 
        more_data_cords ={"cords":convert_cords(data["Coordinates"]),
          "name":data["Name"],
          "CapaciCapacity (MW)":sort_string_to_NONE(data["Capacity (MW)"]),
          "Commissioned":sort_string_to_NONE(data["Commissioned"])}
        stuff.append(more_data_cords)
    return stuff


with open("data/nz_power_stations.json", 'r') as file:
    data_powerpalnts = json.load(file)

with open('data/locations.json', 'r') as file:
    data_locations = json.load(file)


hydro_plants = remake_cords(data_powerpalnts,"Hydroelectric")
Wind_plants = remake_cords(data_powerpalnts,'Wind')
bioenenergy_plants =  remake_cords(data_powerpalnts,'bioenenergy')
Geothermal = remake_cords(data_powerpalnts,'Geothermal')
Fossil_fuel = remake_cords(data_powerpalnts,'Fossil-fuel-thermal')
Solar = remake_cords(data_powerpalnts,'Solar')
# because diferent proccessing the directions hasnt been applied but there are all in the same quadrent


locations = []
for item in data_locations:
    more_data_cords ={"cords":(-1.0*item["latitude"],item["longitude"]),
        "name":item["location"],
        "CapaciCapacity (MW)":None,
        "Commissioned":None}
    locations.append(more_data_cords)

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

rows = []
plt.figure(figsize=(10, 15))

# Setup the axes
plt.xlim(166, 179) 
plt.ylim(-48, -34)
axes = plt.gca()
axes.set_aspect('equal', adjustable='box')

for (label, station_list), color in zip(power_data.items(), colors):
    x_coords = []
    y_coords = []
    sizes = []

    for station in station_list:
        coord = station["cords"]
        
        # Only process if we have a valid tuple
        if isinstance(coord, tuple) and len(coord) == 2:
            lat, lon = coord
            capacity = station["CapaciCapacity (MW)"]
            
            # 1. Add to our Pandas rows list
            rows.append({
                "Name": station["name"],
                "Category": label,
                "Lat": lat,
                "Lon": lon,
                "Capacity_MW": capacity,
                "Commissioned": station["Commissioned"],
                "Color": color
            })
            
            # 2. Prep for plotting
            y_coords.append(lat)
            x_coords.append(lon)
            
            # Use capacity to determine size! 
            # We use a 'min' check so small plants are still visible
            # and divide by a factor so huge plants don't cover the map
            s_val = max(10, capacity / 5) if capacity else 20
            sizes.append(s_val)

    # 3. Plot this category
    if x_coords:
        axes.scatter(x_coords, y_coords, c=color, label=label, s=sizes, alpha=0.6, edgecolors='white', linewidth=0.5)

# Create the DataFrame
df = pd.DataFrame(rows)
df.to_csv("data/NzEnergyGridCapacityAndLocations.csv")

# Add the Legend
plt.legend(title="Station Type", loc='upper left', bbox_to_anchor=(1, 1))
plt.title("New Zealand Power Grid by Capacity")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.savefig('nz_capacity_map.png', bbox_inches='tight')
# print(df.head())
# print(df.tail())
# print(df.info())
grouped = df.groupby("Category")["Capacity_MW"].sum()
sorted_group = grouped.sort_values()
plt.figure(figsize=(12,6))
sorted_group[1::].plot(kind='bar')
print(type(sorted_group))
plt.title("Nz theoretical MW capacity")
plt.xticks(rotation=35, ha='right')
# plt.tight_layout()
plt.grid(True)
plt.xlabel("Energy types")
plt.ylabel("Mw Capacity")
plt.savefig("bar_lot.png")
# print(sorted_group.head())
toatal = sorted_group.sum()
print(toatal)



