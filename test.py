import json
import matplotlib.pyplot as plt
from gemini.regex_extraction import convert_cords
from typing import List, Tuple
with open('data/locations.json', 'r') as file:
    data_locations = json.load(file)

with open("data/nz_power_stations.json", 'r') as file:
    data_powerpalnts = json.load(file)

def remake_cords(data : dict, key: str) -> List[Tuple[float,float]]:
    return [convert_cords(data["Coordinates"])  for data in data_powerpalnts[key]]

hydro_plants = remake_cords(data_powerpalnts,"Hydroelectric")
Wind_plants = remake_cords(data_powerpalnts,'Wind')
bioenenergy_plants =  remake_cords(data_powerpalnts,'bioenenergy')
Geothermal = remake_cords(data_powerpalnts,'Geothermal')
Fossil_fuel = remake_cords(data_powerpalnts,'Fossil-fuel-thermal')
Solar = remake_cords(data_powerpalnts,'Solar')
# because diferent proccessing the directions hasnt been applied but there are all in the same quadrent
locations = [(-1.0*item["latitude"],item["longitude"]) for item in data_locations]


# def plot_lists(data: List[List[Tuple[float,float]]], colors : List[str]) -> None:
#     x_data = []
#     y_data = []
#     color = []
#     for item




# x_data = [item["latitude"] for item in data_locations]
# y_data = [item["longitude"] for item in data_locations]
# plt.figure(figsize=(10,16))
# #NOTE  for filtering later these
# plt.xlim(33,48)
# plt.ylim(167,179)
# axes = plt.gca()
# axes.set_aspect('equal', adjustable='box')
# axes.scatter(x_data,y_data)
# plt.savefig('test.png')
# # print(data)
