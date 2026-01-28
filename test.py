import json
import matplotlib.pyplot as plt
with open('data/locations.json', 'r') as file:
    data= json.load(file)

x_data = [item["latitude"] for item in data]
y_data = [item["longitude"] for item in data]
plt.figure(figsize=(10,16))
#NOTE  for filtering later these
plt.xlim(33,48)
plt.ylim(167,179)
axes = plt.gca()
axes.set_aspect('equal', adjustable='box')
axes.scatter(x_data,y_data)
plt.savefig('test.png')
# print(data)
