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
    data_list = []
    
    # 1. Find the specific container div
    container = soup.find('div', class_=category_class)
    
    if not container:
        print(f"⚠️ Warning: Could not find div with class '{category_class}'")
        raise ValueError("Could not find div with class")


    # 2. Extract Headers
    # CHANGE: We search directly inside the 'container' div, not inside a 'table'
    # We look for all 'th' tags found anywhere inside this div
    headers = [th.get_text(strip=True) for th in container.find_all('th')]
    
    # Quick check: If no headers found, we can't map data
    if not headers:
        print(f"⚠️ No headers found in {category_class}")
        raise ValueError("Could not find headers")

    # 3. Extract Rows
    # CHANGE: We search directly for 'tr' tags inside the div
    # We slice [1:] to skip the first row because it usually contains the headers we just grabbed
    all_rows = container.find_all('tr')
    
    # If the first row contains 'th' tags, we skip it.
    # A safer way than [1:] is to check inside the loop.
    for row in all_rows:
        # Get all cells (td) in this row
        cells = row.find_all('td')
        
        # If there are no 'td' cells, it's likely a header row, so we skip it
        if not cells:
            continue
            
        # 4. The Zip (Pairing data)
        # We need the number of cells to match the number of headers
        if len(cells) == len(headers):
            cell_text = [cell.get_text(strip=True) for cell in cells]
            
            # Create the dictionary
            row_dict = dict(zip(headers, cell_text))
            data_list.append(row_dict)
        else:
            # Optional: Debug print if a row doesn't match headers (e.g. colspan issues)
            # print(f"Skipping row in {category_class}, column count mismatch.")
            pass
            
    return data_list

# --- Test Run ---
# (Run your loop here exactly as before)
all_power_stations = {}
print("Starting extraction...")

for category in categories:
    extracted_data = extract_table_data(soup, category)
    if extracted_data:
        print(f"✅ Success: {category} ({len(extracted_data)} items)")
        all_power_stations[category] = extracted_data

# Export (Same as before)
json_output = json.dumps(all_power_stations, indent=4, ensure_ascii=False)
with open('data/nz_power_stations.json', 'w', encoding='utf-8') as f:
    f.write(json_output)