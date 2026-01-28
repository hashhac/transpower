from requests import Session, Request
from requests.exceptions import RequestException
from typing import Dict
from bs4 import BeautifulSoup
from pathlib import Path
import json
from typing import Tuple, List
def download_html(url:str,data: Dict = None,headers : Dict = None) -> str :
    try:
        session = Session()
        request = Request('Post',url,data=data,headers=headers)
        prepared = request.prepare()
        response = session.send(prepared,stream=False,verify=False,proxies=None,cert=None,timeout=5)
        response.raise_for_status()
        print(response.status_code)
        content = response.text
    except RequestException as e:
        print(f"Error getting data \n{":_^80"}\n{e}")
    return content

def save_html(content : str, path : str):
    with open(path, 'w',encoding='utf-8') as file:
        file.write(content)

def read_html(path : str) -> str:
    with open(path, 'r',encoding='utf-8') as file:
        return file.read()
        


# TODO fix  Rotorao as its way of and formatting has done this also data has mistakes in it needs cleaning steps
def sort_location(map_distance : str) -> Tuple[float,str]:
    '''Returns the map distance from cord format to float and the heading in str '''
    try:
        degrees, deegrees_decimals_heading = map_distance.split("\u00b0")
        # means there are 3 digits 
        #TODO fix issue with backing emojis not reusable code.
        if '\u00e2\u0080\u00b2' in deegrees_decimals_heading :
                 minutes, seconds_heading =  deegrees_decimals_heading.split("\u00e2\u0080\u00b2 ")
                 seconds, heading = seconds_heading.split('\u00e2\u0080\u00b3')
                 distance = float(degrees) + (float(minutes)/60) + (float(seconds)/3600)
                 return (distance,heading)
        #means there are only 2 digits 
        else:
            minutes, heading = deegrees_decimals_heading.split("'")
            distance = float(degrees) + (float(minutes)/60) 
            return (distance,heading)
    except ValueError as e:
        print(f" An error occured trying to split \n{'':_^80}\n {location} \n{'':_^80}\n digits |{map_distance}  \n{'':_^80} {e}")
        exit(1)





data_path = Path('data')
data_path.mkdir(exist_ok=True)



# new_zealand_locations = 'https://www.mapsofworld.com/lat_long/newzealand-lat-long.html'
# content = download_html(new_zealand_locations)
# save_html(content,data_path/"NzLocations.html")
# content = read_html(data_path/"NzLocations.html")
# soup = BeautifulSoup(content, 'html.parser')
# table = soup.find('table', class_='tableizer-table')
# data = []

# for row in table.find_all('tr')[1:]:
#     cols = row.find_all('td')
#     if len(cols) == 3:
#         location = cols[0].get_text(strip=True)
#         latitude = cols[1].get_text(strip=True)
#         longitude = cols[2].get_text(strip=True)
#         latitude_float, latitude_heading =sort_location(latitude)
#         longitude_float, longitude_heading = sort_location(longitude)
#         data.append({
#             "location": location,
#             "latitude": latitude_float,
#             "latitude_heading" : latitude_heading,
#             "longitude": longitude_float,
#             "longitude_heading" :longitude_heading
#         })
# with open(data_path/"locations.json", 'w') as file:
#     json.dump(data,file,indent=3)


content = read_html(data_path/"List of power stations in New Zealand - Wikipedia.html")
soup = BeautifulSoup(content, 'html.parser')
tables = soup.find_all('table')
print(tables)