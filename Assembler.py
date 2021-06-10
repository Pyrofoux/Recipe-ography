import json

from WorldMapGenerator import *
from CultureNameGen import *


# Settings
# They could be stored in a settings.ini file instead

settings = {}
settings["mapgen_iterationCount"]       = 10
settings["mapgen_startMapType"]         = 1


# Starting Assembling

output = {} #output json file
output_file_name = "./webviewer/world_data.js"

# Generates terrain
terrain_map = np.array(generate_terrain_matrix(settings["mapgen_startMapType"], settings["mapgen_iterationCount"]))

output["terrain_steps"] = terrain_map.shape[0] #convert terrain to JSON serializable format
output["terrain_width"] = terrain_map.shape[1]
output["terrain_height"] = terrain_map.shape[2]
output["terrain_map"] = terrain_map.tolist() #convert terrain to JSON serializable format


# Generates culture names
#Culture(1, "The Shire", [250,10,10])

# Saves output file

json_formatted = json.dumps(output)
javascript_content = "let world_data = "+json_formatted

with open(output_file_name, 'w+') as outfile:
    outfile.write(javascript_content)
