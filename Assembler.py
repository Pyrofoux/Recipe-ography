import json

from WorldMapGenerator import *
from CultureNameGen import *
from RecipeGenerator import *
from wordMasher import *


# print(plantDictionary)

# Settings
# They could be stored in a settings.ini file instead



def generateWorldFile(specific_id = None):


    settings = {}
    settings["mapgen_iterationCount"]        = 20
    settings["mapgen_startMapType"]          = 5
    settings["culturespread_iterationCount"] = 100
    settings["number_of_cultures"]           = 5 #Max value is about 12
    settings["max_plants"]                   = 15 #Min = 3*5 = 15

    # Starting Assembling

    output = {} #output json file

    output_file_name = "./webviewer/world_data.js"

    if specific_id != None:
        output_file_name = "./webviewer/pregenerated/world_data_"+str(specific_id)+".js"



    # Generates terrain
    terrain_maps = np.array(generate_terrain_matrix(settings["mapgen_startMapType"], settings["mapgen_iterationCount"]))

    output["terrain_steps"] = terrain_maps.shape[0] #convert terrain to JSON serializable format
    output["terrain_width"] = terrain_maps.shape[1]
    output["terrain_height"] = terrain_maps.shape[2]
    output["terrain_map"] = terrain_map = terrain_maps.tolist()[-1] #Only the last terrain map


    # Generates culture names and borders

    culture_names = generateNameForEachCuisine()[0:settings["number_of_cultures"]]

    cultureList = []

    i = 0
    for name in culture_names:
        i+=1 # Culture id starts at 1
        water_traverser = bool(random.getrandbits(1))
        cultureList.append(Culture(i, name, [i,i,i], water_traverser))

    output["culture_names"] = culture_names

    culture_map =  generate_culture_matrix(terrain_map, cultureList, settings["culturespread_iterationCount"])[0]

    output["culture_map"] = culture_map.tolist()

    # Generates plants library

    plantDictionary = cleanUpDictionary(create_plant_library(original_plants, tileTypes, edible_parts), original_plants)
    output["plantDictionary"] = plantDictionary
    # Generates recipes for each culture, based on soil tile distribution

    tile_ratios = get_tile_ratios_for_cultures(terrain_map, culture_map, cultureList)


    generated_recipes = []

    i = 0
    for culture_name in culture_names:
        i+=1
        tile_ratio = tile_ratios[i]

        #print(tile_ratio)
        generated_recipe = pickRandomRecipe(plantDictionary, functionNumbers, tile_ratio)
        generated_recipes.append(generated_recipe)

    output["recipes"] = generated_recipes



    json_formatted = json.dumps(output)
    javascript_content = "var world_data = "+json_formatted

    with open(output_file_name, 'w+') as outfile:
        outfile.write(javascript_content)



# # To generate the pregenerated worlds for the live demo
# i = 0
# while i < 100:
#     try:
#         generateWorldFile(i)
#         i+=1
#     except:
#         pass

# To generate a single new world
# file will be at webviewer/world_data.js
generateWorldFile()
