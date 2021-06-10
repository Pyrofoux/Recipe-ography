import random
import numpy as np
import math
from enum import Enum, unique
from PIL import Image
from collections import Counter
from PIL import Image, ImageDraw

#-------------------------------------------------------------------------------
#CLASSES & PARAMETERS


#Parameters
MAPSIZE = 100
landChance = 0.5
pixelSize = 10

@unique
class Terrain(Enum):
    WATER = 1
    GRASSLAND = 2
    DESERT = 3
    JUNGLE = 4
    MOUNTAIN = 5
    SNOW = 6

#Define colors of each tile type for basic map generation
#Using RGB color defintions
terrainColors = {Terrain.WATER.value: [3,53,140], Terrain.GRASSLAND.value: [9,156,6], Terrain.DESERT.value: [255,229,99], Terrain.JUNGLE.value: [8,77,0], Terrain.MOUNTAIN.value: [87,75,47], Terrain.SNOW.value:[212,250,248]}

class Culture:
    culture_id = -1
    culture_name = ""
    culture_color = [0,0,0]

    def __init__(self, id, name, color):
        self.culture_id = id
        self.culture_name = name
        self.culture_color = color
#-----------------------------------------------------
#CELLULAR AUTOMATA RULES

#Define Cellular Automata Rules for every terrain type

def water_rules(neighbour_count):
    #If more than 5 neighbours are grassland, return grassland
    if(neighbour_count[Terrain.GRASSLAND.value]>=5):
        return Terrain.GRASSLAND.value
    else:
        return Terrain.WATER.value

def grassland_rules(neighbour_count):
    #If more than 5 neighbours are grassland, return grassland
    if(neighbour_count[Terrain.WATER.value]>=6):
        return Terrain.WATER.value
    #If there are 7 or more grasslands about, have 20% chance of desert, 20% of mountains 
    elif(neighbour_count[Terrain.GRASSLAND.value]>=7):
        choice = random.uniform(0, 1)
        if (choice<0.2):
            return Terrain.MOUNTAIN.value
        elif(choice >0.8):
            return Terrain.DESERT.value
    #Default, return starting value
    return Terrain.GRASSLAND.value

def desert_rules(neighbour_count):
    return Terrain.DESERT.value

def jungle_rules(neighbour_count):
    return Terrain.JUNGLE.value

def mountain_rules(neighbour_count):
    return Terrain.MOUNTAIN.value

def snow_rules(neighbour_count):
    return Terrain.SNOW.value

#Define rules for how culture spread
def culture_spread_rule(cult_neighbour_count, cultureDict, currValue):
    return_culture_id = 0
    max_neighbours = 0
    #Currently, adopt culture of any neighbour
    for key in cultureDict:
        if (cult_neighbour_count[cultureDict[key].culture_id]>max_neighbours):
            return_culture_id = key
            max_neighbours = cult_neighbour_count[cultureDict[key].culture_id]
    choice = random.uniform(0, 1)
    if (choice<(0.1*max_neighbours)):
        return return_culture_id
    #Culture death chance
    #elif(choice>0.8):
        #return 0
    else:
        return currValue

def apply_terrain_rules(mapMatrix):

    updatedMap = np.zeros((len(mapMatrix), len(mapMatrix[0])))

    for i in range(mapMatrix.shape[0]):
        for j in range(mapMatrix.shape[1]):
            neighbour_count = retrieve_neighbours(i,j,mapMatrix)
            if mapMatrix[i][j] == Terrain.WATER.value:
                updatedMap[i][j] = water_rules(neighbour_count)
            elif mapMatrix[i][j] == Terrain.GRASSLAND.value:
                updatedMap[i][j] = grassland_rules(neighbour_count)
            elif mapMatrix[i][j] == Terrain.DESERT.value:
                updatedMap[i][j] = desert_rules(neighbour_count)
            elif mapMatrix[i][j] == Terrain.JUNGLE.value:
                updatedMap[i][j] = jungle_rules(neighbour_count)
            elif mapMatrix[i][j] == Terrain.MOUNTAIN.value:
                updatedMap[i][j] = mountain_rules(neighbour_count)
            elif mapMatrix[i][j] == Terrain.SNOW.value:
                updatedMap[i][j] = snow_rules(neighbour_count)

    return updatedMap

#Run cellular automata rules on whole map X times
#Returns full history (to support pretty gifs)
def terrain_rule_iterations(inputMap, iterationCount):

    map_history = []
    map_history.append(inputMap)

    for i in range(iterationCount):
        inputMap = apply_terrain_rules(inputMap)
        map_history.append(inputMap)
        print("Iteration count: " + repr(i))
    return map_history

def apply_culture_spread_rules(mapMatrix, inputCultureMatrix, cultureList):

    cultureDict = gen_culture_dict(cultureList)

    updatedCultureMap = np.zeros((MAPSIZE, MAPSIZE), dtype=int)

    for i in range(MAPSIZE):
        for j in range(MAPSIZE):
            #Check were not on a water tile or an already set culture 
            if ((not mapMatrix[i][j] == Terrain.WATER.value)):
                culture_neighbour_count = retrieve_neighbours(i,j,inputCultureMatrix)
                updatedCultureMap[i][j] = culture_spread_rule(culture_neighbour_count, cultureDict, inputCultureMatrix[i][j])
    return updatedCultureMap

def culture_spread_iterations(mapMatrix, cultureMatrix, cultureList, iterationCount):

    map_history = []
    map_history.append(cultureMatrix)

    for i in range(iterationCount):
        print("Culture spread iteration count: " + repr(i))
        cultureMatrix = apply_culture_spread_rules(mapMatrix, cultureMatrix, cultureList)
        map_history.append(cultureMatrix)
    return map_history

#-------------------------------------------------------------------------------------
#UTILITY FUNCTIONS

#Retrieve the 3 to 8 neighbouring cells from a matrix
#Returns a dictionary of tile types and the count of instances present
def retrieve_neighbours(i, j, matrix):

    neighbourCells = []
    iRange = [-1,-1]
    jRange = [-1,-1]

    #Determine window to extract
    #Handles if the specified cell is in a corner or on an edge
    if (i>0):
        iRange[0] = i-1
    else:
        iRange[0] = i
    if (i<len(matrix)-1):
        iRange[1] = i+1
    else:
        iRange[1] = i
    
    if (j>0):
        jRange[0] = j-1
    else:
        jRange[0] = j

    if (j<len(matrix)-1):
        jRange[1] = j+1
    else:
        jRange[1] = j

    #print("Irange: " + repr(iRange[0]) + ":" + repr(iRange[1]))
    #print("Jrange: " + repr(jRange[0]) + ":" + repr(jRange[1]))

    for i_it in range(iRange[0], iRange[1]+1):
        for j_it in range(jRange[0], jRange[1]+1):
            #Dont add self
            if (i_it!= i or j_it != j):
                neighbourCells.append(matrix[i_it][j_it])

    return Counter(neighbourCells)

def gen_culture_color_dict(culture_list):
    color_dict = {}
    for i in range(len(culture_list)):
        color_dict[culture_list[i].culture_id] = culture_list[i].culture_color
    return color_dict

def gen_culture_dict(culture_list):
    culture_dict = {}
    for i in range(len(culture_list)):
        culture_dict[culture_list[i].culture_id] = culture_list[i]
    return culture_dict

def pythag(a, b):
    return math.sqrt(a*a + b*b)


#Print world matrix to console
#Mainly for debugging
def display_world(matrix):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] == Terrain.WATER.value:
                print("W", end='')
            elif matrix[i][j] == Terrain.GRASSLAND.value:
                print("G", end='')
            elif matrix[i][j] == Terrain.DESERT.value:
                print("D", end='')
            elif matrix[i][j] == Terrain.JUNGLE.value:
                print("J", end='')                
            elif matrix[i][j] == Terrain.MOUNTAIN.value:
                print("M", end='')                
            elif matrix[i][j] == Terrain.SNOW.value:
                print("S", end='')
        print()

def display_world_int(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            print(matrix[i][j], end='')
        print()

#-------------------------------------------------------------------------------------
#IMAGE GENERATION

def gen_img_from_map_matrix(matrix):      

    return Image.fromarray(get_world_rgb_from_map_matrix(matrix), 'RGB')

def get_world_rgb_from_map_matrix(matrix):
    w, h = len(matrix)*pixelSize, len(matrix[0])*pixelSize
    data = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            i1 = (i*pixelSize)
            i2 = ((i+1)*pixelSize)
            j1 = (j*pixelSize)
            j2 = ((j+1)*pixelSize)
            if matrix[i][j] == Terrain.WATER.value:
                data[i1:i2,j1:j2] = terrainColors[Terrain.WATER.value]
            elif matrix[i][j] == Terrain.GRASSLAND.value:
                data[i1:i2,j1:j2]  = terrainColors[Terrain.GRASSLAND.value]
            elif matrix[i][j] == Terrain.DESERT.value:
                data[i1:i2,j1:j2]  = terrainColors[Terrain.DESERT.value]
            elif matrix[i][j] == Terrain.JUNGLE.value:
                data[i1:i2,j1:j2]  = terrainColors[Terrain.JUNGLE.value]               
            elif matrix[i][j] == Terrain.MOUNTAIN.value:
                data[i1:i2,j1:j2]  = terrainColors[Terrain.MOUNTAIN.value]                 
            elif matrix[i][j] == Terrain.SNOW.value:
                data[i1:i2,j1:j2]  = terrainColors[Terrain.SNOW.value]   
    return data

def gen_img_from_culture_and_terrain_matrix(terrain_map, culture_map, culture_list):
    return Image.fromarray(get_culture_and_terrain_rgb(terrain_map, culture_map, culture_list), 'RGB')

def get_culture_and_terrain_rgb(terrain_map, culture_map, culture_list):
    culture_pixel_offset = 2

    terrain_rgb_map = get_world_rgb_from_map_matrix(terrain_map)

    color_dict = gen_culture_color_dict(culture_list)

    for i in range(culture_map.shape[0]):
        for j in range(culture_map.shape[1]):
            #Add culture color to map if it exists in dictionary
            if (culture_map[i][j] in color_dict):
                culture_color = color_dict[culture_map[i][j]]
                #Generate coordinates of culture color square
                i1 = (i*pixelSize)+culture_pixel_offset
                i2 = ((i+1)*pixelSize)-culture_pixel_offset
                j1 = (j*pixelSize)+culture_pixel_offset
                j2 = ((j+1)*pixelSize)-culture_pixel_offset
                terrain_rgb_map[i1:i2,j1:j2] = culture_color
    return terrain_rgb_map


def get_culture_from_array(cultures, id):
    return_culture = None
    for i in range(len(cultures)):
        if (cultures[i].culture_id == id):
            return_culture = cultures[i]
    return return_culture

def save_terrain_history_gif(inputMaps, savePath):

    mapImages = []
    for i in range(len(inputMaps)-1):
        mapImages.append(gen_img_from_map_matrix(inputMaps[i]))
    mapImages[0].save(savePath, save_all=True, append_images = mapImages[1:], optimize=False, duration=500, loop=0)

def save_culture_history_gif(terrainMap, cultureHistory, cultureList, savePath):
    images = []
    for i in range(len(cultureHistory)-1):
        images.append(gen_img_from_culture_and_terrain_matrix(terrainMap, cultureHistory[i],cultureList))
    images[0].save(savePath, save_all=True, append_images = images[1:], optimize=False, duration=50, loop=0)
#-----------------------------------------------------------------------------------------
#INITIAL MAP GENERATION FUNCTIONS

#Generate a starting map
#Comprised of random static out of water and grassland tiles
def gen_noise_map():
    #Instantiate matrix representing our world map
    mapSize = (MAPSIZE,MAPSIZE)

    new_map = np.ones(mapSize)
    for i in range(len(new_map)):
        for j in range(len(new_map[0])):
            # choose a number between 0-1
            choice = random.uniform(0, 1)
            # choose a WATER or GRASSLAND
            if choice < landChance:
                new_map[i][j] = Terrain.GRASSLAND.value
            else:
                new_map[i][j] = Terrain.WATER.value
    print("Starting map generated")
    return new_map

def gen_central_island_start_map():
    #Instantiate matrix representing our world map
    mapSize = (MAPSIZE,MAPSIZE)

    new_map = np.ones(mapSize)
    for i in range(len(new_map)):
        for j in range(len(new_map[0])):


            #Increased change of grass closer to the centre of the map
            #Calculate distance of i and j to the centre, normalised between 0 and 1
            mapRadius = MAPSIZE/2
            iCentreDist = (abs(i-mapRadius))/mapRadius
            jCentreDist = (abs(j-mapRadius))/mapRadius

            centreDist = pythag(iCentreDist,jCentreDist)

            grasslandChance = centreDist-0.1

            # choose a number between 0-1
            choice = random.uniform(0, 1)

            if choice > grasslandChance:
                new_map[i][j] = Terrain.GRASSLAND.value
            else:
                new_map[i][j] = Terrain.WATER.value
    print("Starting map generated")
    return new_map

def gen_culture_start_map(terrainMap, start_cultures):
    
    width = len(terrainMap)
    height = len(terrainMap[0])

    culture_map = np.zeros((width, height), dtype=int)

    #Loop through all cultures and place them
    for i in range(len(start_cultures)):
        culture_to_place = start_cultures[i]
        culture_set = False
        while(not culture_set):
            #pick random coordinates
            i = random.randint(0, width-1)
            j = random.randint(0, height-1)
            #Check if were on land and not in a ocupied cell
            if((not terrainMap[i][j] == Terrain.WATER.value) and (culture_map[i][j] == 0)):
                print("Settling culture " + repr(culture_to_place.culture_name) + " in cell: " + repr(i) +"," + repr(j))
                culture_map[i][j] = int(culture_to_place.culture_id)
                culture_set = True
    return culture_map

#-------------------------------------------------------------------------------------------------------------------------------------#
#FULL RUN METHODS
def generate_terrain_matrix(startMapType, iterationCount):
    startMap = np.zeros((MAPSIZE, MAPSIZE), dtype=int)
    #Decide on start map type
    if (startMapType==1):
        startMap = gen_noise_map()
    elif (startMapType==2):
        startMap = gen_central_island_start_map()
    else:
        startMap = gen_noise_map()
    return terrain_rule_iterations(startMap, iterationCount)

def generate_culture_matrix(terrainMap, cultureList, iterationCount):
    culture_start_positions = gen_culture_start_map(terrainMap, cultureList)
    return culture_spread_iterations(terrainMap,culture_start_positions, cultureList, iterationCount)


#-------------------------------------------------------------------------------------------------------------------------------------#

#TESTING


image_save_path = 'C:/Users/Ollie/Documents/ACADEMIA/IGGI PHD/Year 1 Modules/Game Dev 2/Food Maps Project/Output Images/'

#TESTING CENTRAL ISLAND GENERATION
twenty_gen_map = generate_terrain_matrix(1, 20)

final_map = twenty_gen_map[len(twenty_gen_map)-1]

gen_img_from_map_matrix(final_map).show()
save_terrain_history_gif(twenty_gen_map, (image_save_path+'TestCentralOutput.gif'))

test_cultures = []
test_cultures.append(Culture(1, "The Shire", [250,10,10]))
test_cultures.append(Culture(2, "Mordor", [10,46,250]))
test_cultures.append(Culture(3, "Rohan", [255,234,0]))
test_cultures.append(Culture(4, "The Elves", [255,36,237]))

#test_culture_map = gen_culture_start_map(final_map, test_cultures)

#display_world_int(test_culture_map)

#culture_rgb_map = get_culture_and_terrain_rgb(final_map, test_culture_map, test_cultures)

#Image.fromarray((culture_rgb_map)).show()

#print(test_culture_map.shape[0])

thirty_culture_spreads = generate_culture_matrix(final_map,test_cultures,200)

final_culture_map = thirty_culture_spreads[len(thirty_culture_spreads)-1]

#display_world_int(final_culture_map)

Image.fromarray(get_culture_and_terrain_rgb(final_map,final_culture_map,test_cultures)).show()
save_culture_history_gif(final_map,thirty_culture_spreads,test_cultures, (image_save_path+'CultureSpread.gif'))

#TESTING FULLY RANDOM MAP GENERATION

#start_map = gen_noise_map()
#get_world_image(start_map).show()
#twenty_gen_map = terrain_rule_iterations(start_map, 20)
#get_world_image(twenty_gen_map[len(twenty_gen_map)-1]).show()
#save_terrain_history_gif(twenty_gen_map, (image_save_path+'TestOutput.gif'))

