import json

from WorldMapGenerator import *
from CultureNameGen import *


# Settings
# They could be stored in a settings.ini file instead

settings = {}
settings["mapgen_iterationCount"]        = 10
settings["mapgen_startMapType"]          = 1
settings["culturespread_iterationCount"] = 100


# Starting Assembling

output = {} #output json file
output_file_name = "./webviewer/world_data.js"

# Generates terrain
terrain_maps = np.array(generate_terrain_matrix(settings["mapgen_startMapType"], settings["mapgen_iterationCount"]))

output["terrain_steps"] = terrain_maps.shape[0] #convert terrain to JSON serializable format
output["terrain_width"] = terrain_maps.shape[1]
output["terrain_height"] = terrain_maps.shape[2]
output["terrain_map"] = terrain_map = terrain_maps.tolist()[-1] #Only the last terrain map


# Generates culture names


culture_names = ["The Shire","Mordor","Rohan","The Elves"]

cultureList = []

i = 0
for name in culture_names:
    i+=1 # Culture id starts at 1
    cultureList.append(Culture(i, name, [i,i,i]))


output["culture_names"] = culture_names

culture_maps = generate_culture_matrix(terrain_map, cultureList, settings["culturespread_iterationCount"])

culture_map = culture_maps[-1]
output["culture_map"] = culture_map.tolist()

json_formatted = json.dumps(output)
javascript_content = "let world_data = "+json_formatted

with open(output_file_name, 'w+') as outfile:
    outfile.write(javascript_content)
