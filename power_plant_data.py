# GEMINI CODE 
from bs4 import BeautifulSoup
import json
from pathlib import Path
def read_html(path : str) -> str:
    with open(path, 'r',encoding='utf-8') as file:
        return file.read()
data_path = Path('data')
data_path.mkdir(exist_ok=True)
content = read_html(data_path/"List of power stations in New Zealand - Wikipedia.html")
soup = BeautifulSoup(content, 'html.parser')
tables = soup.find_all('table')
print(tables)
# 1. Setup: Your list of categories (matching the div classes you made)
categories = [
    "Hydroelectric", "Wind", "bioenenergy", "Geothermal",
    "Fossil-fuel-thermal", "Solar", "grid-battery-storage", "future"
]

# (Assuming 'soup' is already loaded as per your snippet)
# For testing, I'm assuming 'soup' contains the HTML structure you pasted.

def extract_table_data(soup, category_class):
    """
    Finds a div with a specific class, looks for a table inside,
    and converts it to a list of dictionaries.
    """
    data_list = []
    
    # Step A: Find the specific container div
    container = soup.find('div', class_=category_class)
    
    # Safety Check: If the div doesn't exist (maybe a typo?), return empty
    if not container:
        print(f"⚠️ Warning: Could not find div with class '{category_class}'")
        return []

    # Step B: Find the table inside that div
    table = container.find('table')
    if not table:
        return []

    # Step C: Extract Headers dynamically
    # We look for 'th' inside 'thead'. 
    # .get_text(strip=True) removes newlines and extra spaces.
    headers = [th.get_text(strip=True) for th in table.select('thead th')]
    
    # Step D: Extract Rows
    # We look for 'tr' inside 'tbody'
    rows = table.select('tbody tr')
    for row in rows:
        # Find all cells in the row. Sometimes data is in <td>, sometimes <th>
        cells = row.find_all(['td', 'th'])
        
        # We only want rows that actually match our header count
        if len(cells) == len(headers):
            # The Magic: clear the text and pair it with the header
            cell_text = [cell.get_text(strip=True) for cell in cells]
            
            # zip(headers, cell_text) pairs them up: ('Name', 'Glen Innes')
            row_dict = dict(zip(headers, cell_text))
            data_list.append(row_dict)
            
    return data_list

# 2. The Execution Loop
all_power_stations = {}

print("Starting extraction...")

for category in categories:
    print(f"Processing: {category}")
    # Call our function
    extracted_data = extract_table_data(soup, category)
    # Add to our master dictionary
    all_power_stations[category] = extracted_data

# 3. Export to JSON
# ensure_ascii=False allows special characters (like Māori names) to print correctly
json_output = json.dumps(all_power_stations, indent=4, ensure_ascii=False)

# Saving to a file
with open(f'data/nz_power_stations.json', 'w', encoding='utf-8') as f:
    f.write(json_output)

print("Done! Data saved to nz_power_stations.json")