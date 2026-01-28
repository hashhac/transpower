from dataclasses import dataclass
from typing import Tuple, List 
from enum import Enum , auto
# TRANS POWER PLANTS 

class PowerGen(Enum):
    hydropower = auto()
    geothermal = auto()
    wind = auto()
    natural_gas = auto()
    coal = auto()
    solar = auto()
#dot classes 
@dataclass
class PowerPlant():
    def __init__ (self,plant_name : str, power_generation : float, generation_type : PowerGen):
        self.name : str = plant_name
        self.generation : float = power_generation
        self.generation_type : PowerGen = generation_type

@dataclass
class Location:
    def __init__ (self, name):
        self.name : str = name

# overall classes
@dataclass
class NewZealand():
    def __intit__ (self):
        self.locations : List = []
        self.power_plants : List = []
        self.connections : List = []
    def add_location(self, latitude : float, longitude : float, loaction : Location):
        self.locations.append({"place" : loaction, "latitude" : latitude, "longitude" : longitude})
    def add_Plant(self,  latitude : float, longitude : float, plant : PowerPlant):
        self.PowerPlant.append({"place" : PowerPlant, "latitude" : latitude, "longitude" : longitude})
    def add_connection(self, location :Location, other_location : Location):
        if (location in self.locations ) and (other_location in self.locations):
            self.connections.append((location,other_location))
# TODO re-write this so each location owns a power plant or multiple and then has infastrcuter etc and then construct a strcut of locations would be better.
# TODO THIS IS TO much work for this right now as I need transmision lines data, and the demand data which i dont have at this time.

    