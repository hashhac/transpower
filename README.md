# This was a Transpower proof of concept.
This project is to express my interest in the role of Associate Grid Investment Modeller.
## Installation
`git clone https://github.com/hashhac/transpower.git`
`pip install -r requirements.txt`

### Requirements
python 3.10 + 

### Results
* Starting with the idea of modeling a digital twin, I eagerly laid out the groundwork for creating a fully functional series of classes that would integrate for some really cool power modeling.
* ```python
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
  ```
* However, I soon realised there was no easily accessible data available, so the project moved to getting data.
  * I found a website with locations which I thought might roughly give me the [locations](https://www.mapsofworld.com/lat_long/newzealand-lat-long.html) of New Zealand as a starting point.
  * I then needed to convert the data and make it usable, converting it from its ordinary latitude and longitude to a floating point format, which took some learning, before then type casting it to a float.
  * For generation I scrapped the wiki page for the power generation data [wiki](https://en.wikipedia.org/wiki/List_of_power_stations_in_New_Zealand), which proved trickier than I thought, as all the tables were different, but it had fewer mistakes.
* Plotting the data after a few iterations, from just locations to locations and generation to adjusting size, I arrived at.
  <img width="640" height="480" alt="test" src="https://github.com/user-attachments/assets/8e641f45-42c3-4b07-8811-eaaa398e929b" />
* Here I realised my data didn't lead to much, and so I refactored it to allow for a more complete set of data to be saved as a CSV so that anyone else can do this quickly and easily too. [Check](https://github.com/hashhac/transpower/blob/main/data/NzEnergyGridCapacityAndLocations.csv) which is ->  `data/NzEnergyGridCapacityAndLocations.csv` in the github
  <img width="998" height="920" alt="nz_capacity_map" src="https://github.com/user-attachments/assets/dd561115-29f2-4023-8a12-1922a1a36335" />
* With the overall graph of NZ plotted, I also wanted to see how clean my data was, as it was missing lots of generation sites and other bits of information.
* I assumed that anything in my data was valid. Still, I am aware this isn't accurate, as lots of the plants on the wiki page were decommissioned or had missing values. It entirely ignores the movement of energy through the grid, so how accurate this is, well, is anyone's guess. A future project would be a nice way to put it.
  <img width="1200" height="600" alt="bar_lot" src="https://github.com/user-attachments/assets/adf91fd8-a417-47b3-9fb1-f049b27baf83" />
* The total from the graph came to: 11486.16 MW.
