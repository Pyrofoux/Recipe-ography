import random
import numpy as np
import math
from enum import Enum, IntEnum, unique
from PIL import Image
from collections import Counter
from PIL import Image, ImageDraw
from perlin_noise import PerlinNoise

#-------------------------------------------------------------------------------
#CLASSES & PARAMETERS


#Parameters
MAPSIZE = 100
landChance = 0.5
pixelSize = 10

@unique
class Terrain(IntEnum):
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
    culture_can_traverse_water = False

    def __init__(self, id, name, color, water_traverser):
        self.culture_id = id
        self.culture_name = name
        self.culture_color = color
        self.culture_can_traverse_water = water_traverser
#-----------------------------------------------------
#CELLULAR AUTOMATA RULES

#Define Cellular Automata Rules for every terrain type

def water_rules(neighbour_count):
    return_tiletype = Terrain.WATER.value
    #If four or less neighbours are water, turn into grassland with X chance
    #if(neighbour_count[Terrain.WATER.value]<=4):
    #    choice = random.uniform(0, 1)
    #    if (choice<0.5):
    #        return_tiletype = Terrain.GRASSLAND.value
    return_tiletype = multiuse_jungle_spread_rule(neighbour_count,return_tiletype)
    return_tiletype = multiuse_desert_spread_rule(neighbour_count,return_tiletype)
    return_tiletype = multiuse_snow_spread_rule(neighbour_count, return_tiletype)
    return_tiletype = multiuse_grass_spread_rule(neighbour_count,return_tiletype)
    return return_tiletype

def grassland_rules(neighbour_count):

    return_tiletype = Terrain.GRASSLAND.value

    return_tiletype = multiuse_jungle_spread_rule(neighbour_count,return_tiletype)
    return_tiletype = multiuse_desert_spread_rule(neighbour_count,return_tiletype)
    return_tiletype = multiuse_snow_spread_rule(neighbour_count, return_tiletype)
    return_tiletype = multiuse_grass_spread_rule(neighbour_count,return_tiletype)
    return_tiletype = multiuse_mountain_spawn_and_chain_rule(neighbour_count,return_tiletype)
    return_tiletype= multiuse_water_spread_rule(neighbour_count,return_tiletype)

    #Default, return starting value
    return return_tiletype

def desert_rules(neighbour_count):
    return_tiletype = Terrain.DESERT.value

    #If theres water nearby, chance of switching back to grassland
    #if(neighbour_count[Terrain.WATER.value]>=1):
    #    choice = random.uniform(0, 1)
    #    if (choice<0.5):
    #        return_tiletype = Terrain.GRASSLAND.value
    #Small chance of grassland spreading
    #elif(neighbour_count[Terrain.GRASSLAND.value]>=1):
    #    choice = random.uniform(0, 1)
    #    if (choice<0.1):
    #        return_tiletype = Terrain.GRASSLAND.value
    return_tiletype = multiuse_jungle_spread_rule(neighbour_count,return_tiletype)
    return_tiletype = multiuse_snow_spread_rule(neighbour_count, return_tiletype)
    return_tiletype = multiuse_grass_spread_rule(neighbour_count,return_tiletype)
    return_tiletype = multiuse_mountain_spawn_and_chain_rule(neighbour_count,return_tiletype)
    return_tiletype = multiuse_water_spread_rule(neighbour_count,return_tiletype)
    return return_tiletype

def jungle_rules(neighbour_count):
    return_tiletype = Terrain.JUNGLE.value

    return_tiletype = multiuse_snow_spread_rule(neighbour_count, return_tiletype)
    return_tiletype = multiuse_desert_spread_rule(neighbour_count,return_tiletype)
    return_tiletype = multiuse_grass_spread_rule(neighbour_count,return_tiletype)
    return_tiletype = multiuse_mountain_spawn_and_chain_rule(neighbour_count,return_tiletype)
    return_tiletype = multiuse_water_spread_rule(neighbour_count,return_tiletype)
    return return_tiletype

def mountain_rules(neighbour_count):
    return_tiletype = Terrain.MOUNTAIN.value
    #If theres too many mountains around,  x %chance of turn into most common neighbour
    if(neighbour_count[Terrain.MOUNTAIN.value]>=4):
        choice = random.uniform(0, 1)
        if (choice<0.5):
            return_tiletype= get_most_commom_tiletype_from_neighbours(neighbour_count, Terrain.MOUNTAIN.value)
    #Flat chance for any mountain to destroy itself
    else:
        choice = random.uniform(0, 1)
        if (choice<0.1):
            return_tiletype = get_most_commom_tiletype_from_neighbours(neighbour_count, Terrain.MOUNTAIN.value)
    return_tiletype = multiuse_water_spread_rule(neighbour_count,return_tiletype)
    return return_tiletype

def snow_rules(neighbour_count):
    return_tiletype = Terrain.SNOW.value
    return_tiletype = multiuse_desert_spread_rule(neighbour_count,return_tiletype)
    return_tiletype = multiuse_jungle_spread_rule(neighbour_count,return_tiletype)
    return_tiletype = multiuse_grass_spread_rule(neighbour_count,return_tiletype)
    return_tiletype = multiuse_mountain_spawn_and_chain_rule(neighbour_count,return_tiletype)
    return_tiletype = multiuse_water_spread_rule(neighbour_count,return_tiletype)
    return return_tiletype


def multiuse_mountain_spawn_and_chain_rule(neighbour_count, input_value):
    return_tiletype = input_value
    #If theres 1, 2 or 3 local mountains, chance of becoming one
    if(neighbour_count[Terrain.MOUNTAIN.value] in (1,2,3) ):
        choice = random.uniform(0, 1)
        if (choice<0.05):
            return_tiletype = Terrain.MOUNTAIN.value
    #If 2 or less neighbouring tiles are water, chance of spawning mountains
    if(neighbour_count[Terrain.WATER.value]<=1):
        choice = random.uniform(0, 1)
        if (choice<0.001):
            return_tiletype = Terrain.MOUNTAIN.value
    return return_tiletype

#If more than X water tiles near by, X% chance of spreading
def multiuse_water_spread_rule(neighbour_count, input_value):
    #Rather than a fixed number, instead spread if more than half neighbours are water
    #This is to stop water being erradicated at the map boundry
    if(neighbour_count[Terrain.WATER.value]>=4):
    #if(neighbour_count.most_common(1)[0][0] == Terrain.WATER.value):
        choice = random.uniform(0, 1)
        #Base odds on amount of tiles of type nearby
        bound = (0.06 *neighbour_count[Terrain.WATER.value])
        if (choice<bound):
            return Terrain.WATER.value
    #Default, return self
    return input_value

def multiuse_grass_spread_rule(neighbour_count, input_value):
    if(neighbour_count[Terrain.GRASSLAND.value]>=3):
        choice = random.uniform(0, 1)
        #Base odds on amount of tiles of type nearby
        bound = (0.07 *neighbour_count[Terrain.GRASSLAND.value])
        if (choice<bound):
            return Terrain.GRASSLAND.value
    #Default, return self
    return input_value

def multiuse_snow_spread_rule(neighbour_count, input_value):
    if(neighbour_count[Terrain.SNOW.value]>=4):
        choice = random.uniform(0, 1)
        #Base odds on amount of tiles of type nearby
        bound = (0.15 *neighbour_count[Terrain.SNOW.value])
        if (choice>bound):
            return Terrain.SNOW.value
    #Default, return self
    return input_value

def multiuse_jungle_spread_rule(neighbour_count, input_value):
    if(neighbour_count[Terrain.JUNGLE.value]>=3):
        choice = random.uniform(0, 1)
        #Base odds on amount of tiles of type nearby
        bound = (0.12 *neighbour_count[Terrain.JUNGLE.value])
        if (choice>bound):
            return Terrain.JUNGLE.value
    #Default, return self
    return input_value

def multiuse_desert_spread_rule(neighbour_count, input_value):
    if(neighbour_count[Terrain.DESERT.value]>=3):
        choice = random.uniform(0, 1)
        #Base odds on amount of tiles of type nearby
        bound = (0.12 *neighbour_count[Terrain.DESERT.value])
        if (choice>bound):
            return Terrain.DESERT.value
    #Default, return self
    return input_value

#Define rules for how culture spread
def culture_spread_rule(cult_neighbour_count, cultureDict, currValue, terrainType):
    return_culture_id = currValue
    max_neighbours = 0
    #Remove 0s from neighbour count
    #print("Neighbours with zeroes: " + repr(cult_neighbour_count))
    del cult_neighbour_count[0]
    #print("Neighbours no zeroes: " + repr(cult_neighbour_count))

    #Stochastic selection of neighbour culture to spread
    #Weighted to favour more common cultures
    #Check if dictionary is empty
    #Only run if current value is 0 (no culture present)
    if (cult_neighbour_count and (currValue == 0)):
        sum_neighbour = sum(cult_neighbour_count.values())
        target = random.uniform(0,sum_neighbour+1)
        curr_sum = 0
        culture_selected = False
        for key in cultureDict:
            curr_sum += cult_neighbour_count[cultureDict[key].culture_id]
            #print("Curr_Sum: " + repr(curr_sum) + " Target: " + repr(target))
            if (curr_sum>target and (not culture_selected)):
                culture_selected = True
                return_culture_id = key

        #Check if we have assigned a culture
        if (not return_culture_id == 0):
            #Determine odds of spreading based on tile type
            choice = random.uniform(0, 1)
            #IF grassland  100% spread
            if (terrainType==Terrain.GRASSLAND.value):
                return return_culture_id
            #If water and amphibious 20% spread
            elif (terrainType==Terrain.WATER.value and (cultureDict[return_culture_id].culture_can_traverse_water)):
                if (choice<0.2):
                    return return_culture_id
                else:
                    return currValue
            #If jungle, desert of snow, 50% chance of spreading
            elif (terrainType==Terrain.DESERT.value or terrainType==Terrain.JUNGLE.value or terrainType==Terrain.SNOW.value):
                if (choice<0.1):
                    return return_culture_id
                else:
                    return currValue
            #If Mountains, 10% chance of traverse
            elif (terrainType==Terrain.MOUNTAIN.value):
                if (choice<0.01):
                    return return_culture_id
                else:
                    return currValue
            else:
                return currValue
        else:
            return currValue
    else:
        return currValue

def apply_terrain_rules(mapMatrix):

    updatedMap = np.zeros((MAPSIZE, MAPSIZE), dtype=int)

    for i in range(MAPSIZE):
        for j in range(MAPSIZE):
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
        #print("Iteration count: " + repr(i))
    return map_history

def apply_culture_spread_rules(mapMatrix, inputCultureMatrix, cultureList):

    cultureDict = gen_culture_dict(cultureList)

    updatedCultureMap = np.zeros((MAPSIZE, MAPSIZE), dtype=int)

    for i in range(MAPSIZE):
        for j in range(MAPSIZE):
            culture_neighbour_count = retrieve_neighbours(i,j,inputCultureMatrix)
            updatedCultureMap[i][j] = culture_spread_rule(culture_neighbour_count, cultureDict, inputCultureMatrix[i][j], mapMatrix[i][j])
    return updatedCultureMap

def culture_spread_iterations(mapMatrix, cultureMatrix, cultureList, iterationCount):

    map_history = []
    map_history.append(cultureMatrix)

    for i in range(iterationCount):
        #print("Culture spread iteration count: " + repr(i))
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

def get_most_commom_tiletype_from_neighbours(counter, selfType):
    maxvalue = -1
    return_id = -1
    for key in counter:
        if (counter[key]>maxvalue and (not key== selfType)):
         maxvalue = counter[key]
         return_id = key
    return return_id

#Remove all culture on water tiles
def tidy_culture_on_water(mapMatrix, cultureMatrix):
    updatedCultureMap = np.zeros((MAPSIZE, MAPSIZE), dtype=int)

    for i in range(MAPSIZE):
        for j in range(MAPSIZE):
            if (mapMatrix[i][j]==Terrain.WATER.value):
                updatedCultureMap[i][j] = 0
            else:
                updatedCultureMap[i][j] = cultureMatrix[i][j]
    return updatedCultureMap


#Remove holes in the cultureMatrix
def tidy_culture_holes(cultureMatrix):
    updatedCultureMap = np.zeros((MAPSIZE, MAPSIZE), dtype=int)

    for i in range(MAPSIZE):
        for j in range(MAPSIZE):

            neighbours_count = retrieve_neighbours(i,j,cultureMatrix)
            updatedCultureMap[i][j] = cultureMatrix[i][j]
            
            if cultureMatrix[i][j] == 0:

                for culture_id in neighbours_count:
                    if neighbours_count[culture_id] >= 4 and culture_id > 0:
                        updatedCultureMap[i][j] = culture_id


    return updatedCultureMap



def gen_tiletype_count_dictionary():
    tileDict = {}
    for type in Terrain:
        tileDict[type.value] = 0
    return tileDict

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
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
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
    map_dimensions = (MAPSIZE,MAPSIZE)

    new_map = np.ones(map_dimensions)
    for i in range(MAPSIZE):
        for j in range(MAPSIZE):


            #Increased change of grass closer to the centre of the map
            #Calculate distance of i and j to the centre, normalised between 0 and 1
            mapRadius = MAPSIZE/2
            iCentreDist = (abs(i-mapRadius))/mapRadius
            jCentreDist = (abs(j-mapRadius))/mapRadius

            centreDist = pythag(iCentreDist,jCentreDist)

            grasslandChance = centreDist-0.2

            # choose a number between 0-1
            choice = random.uniform(0, 1)

            if choice > grasslandChance:
                new_map[i][j] = Terrain.GRASSLAND.value
            else:
                new_map[i][j] = Terrain.WATER.value
    print("Starting map generated")
    return new_map

def gen_perlin_noise_map():
    noise1 = PerlinNoise(octaves=3)
    noise2 = PerlinNoise(octaves=6)
    noise3 = PerlinNoise(octaves=12)
    noise4 = PerlinNoise(octaves=24)

    new_map = []
    for i in range(MAPSIZE):
        row = []
        for j in range(MAPSIZE):
            noise_val =         noise1([i/MAPSIZE, j/MAPSIZE])
            noise_val += 0.5  * noise2([i/MAPSIZE, j/MAPSIZE])
            noise_val += 0.25 * noise3([i/MAPSIZE, j/MAPSIZE])
            noise_val += 0.125* noise4([i/MAPSIZE, j/MAPSIZE])

            row.append(noise_val)
        new_map.append(row)
    #Make noise terrainy
    for i in range(MAPSIZE):
        for j in range(MAPSIZE):
            #Add uncertainty to make boundries fuzzier
            choice = random.uniform(0, 0.1)
            if(choice<new_map[i][j]):
                new_map[i][j] = Terrain.GRASSLAND.value
            else:
                new_map[i][j] = Terrain.WATER.value

            #if (new_map[i][j]>0.06):
            #    new_map[i][j] = Terrain.GRASSLAND.value
            #else:
            #    new_map[i][j] = Terrain.WATER.value
    return new_map

def gen_banded_noise_map():
    return terrain_band_map(gen_noise_map())

def gen_banded_central_map():
    return terrain_band_map(gen_central_island_start_map())

def gen_banded_perlin_map():
    return terrain_band_map(gen_perlin_noise_map())

#Process a terrain map, and impose terrain bands on it
#Intended to alter the initial seed map which starts the generation
def terrain_band_map(terrainMap):
    bands = np.linspace(0, MAPSIZE, 8, dtype=int)

    for i in range(MAPSIZE):
        for j in range(MAPSIZE):
            if (not terrainMap[i][j] == Terrain.WATER.value):
                #Set snow for upper and lower bounds
                if ((bands[0]<=i<=bands[1]) or (bands[6]<i<bands[7])):
                    terrainMap[i][j] = Terrain.SNOW.value
                #Set grassland for 2nd inner bounds
                elif ((bands[1]<i<=bands[2]) or (bands[5]<=i<bands[6])):
                    terrainMap[i][j] = Terrain.GRASSLAND.value
                elif ((bands[2]<i<=bands[3]) or (bands[4]<=i<bands[5])):
                    terrainMap[i][j] = Terrain.JUNGLE.value
                elif (bands[3]<i<bands[4]):
                    terrainMap[i][j] = Terrain.DESERT.value
                #Default (should never be reached)
                else:
                    terrainMap[i][j] = Terrain.GRASSLAND.value
    return terrainMap

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
    elif (startMapType==3):
        startMap = gen_banded_noise_map()
    elif (startMapType==4):
        startMap = gen_banded_central_map()
    elif (startMapType==5):
        startMap = gen_banded_perlin_map()
    else:
        startMap = gen_noise_map()
    return terrain_rule_iterations(startMap, iterationCount)

def generate_culture_matrix(terrainMap, cultureList, iterationCount):
    culture_start_positions = gen_culture_start_map(terrainMap, cultureList)
    fullHistory = culture_spread_iterations(terrainMap,culture_start_positions, cultureList, iterationCount)
    tidied_water = tidy_culture_on_water(terrainMap, fullHistory[-1])
    tidied_holes = tidy_culture_holes(tidied_water)
    return (tidied_holes,fullHistory)


#Get tile ratios from culture
def get_tile_ratios_for_cultures(mapMatrix, cultureMatrix, cultureList):
    #Array of tile dictionaries for each culture
    output = {}
    for culture in cultureList:
        culture_tile_count = gen_tiletype_count_dictionary()
        for i in range(MAPSIZE):
            for j in range(MAPSIZE):
                if (cultureMatrix[i][j]==culture.culture_id ):
                    #Adjust return ratios based on tile type
                    if (mapMatrix[i][j]==Terrain.GRASSLAND.value):
                        culture_tile_count[mapMatrix[i][j]]+=1
                    elif (mapMatrix[i][j] == Terrain.JUNGLE.value or mapMatrix[i][j] == Terrain.DESERT.value or mapMatrix[i][j] == Terrain.SNOW.value):
                        culture_tile_count[mapMatrix[i][j]]+=2
                    elif (mapMatrix[i][j] == Terrain.MOUNTAIN.value):
                        culture_tile_count[mapMatrix[i][j]]+=5
        #print("Pre normalised:")
        #print(culture_tile_count)
        #Get sum total, for ensuring values add up to 100
        sumValues = 0
        for key in culture_tile_count:
            sumValues += culture_tile_count[key]
        #Adjust so values add up to 100
        for key in culture_tile_count:
            culture_tile_count[key] = (culture_tile_count[key]/sumValues)*100
        #print("Post normalised with sum max " + repr(sumValues) + ":")
        #print(culture_tile_count)
        #Add to output
        output[culture.culture_id] = culture_tile_count
    return output



#-------------------------------------------------------------------------------------------------------------------------------------#


# This line says that everything after will only be executed if you run the script directly,
# and will not be run if you load the script from another module, like the Assembler :)
if __name__ == "__main__":

    #TESTING
    image_save_path = 'C:/Users/Ollie/Documents/ACADEMIA/IGGI PHD/Year 1 Modules/Game Dev 2/Food Maps Project/Output Images/'


    #test_start = gen_perlin_noise_map()
    #Image.fromarray(get_world_rgb_from_map_matrix(test_start)).show()
    #banded_start = terrain_band_map(test_start)
    #Image.fromarray(get_world_rgb_from_map_matrix(banded_start)).show()

    #TESTING ISLAND GENERATION
    twenty_gen_map = generate_terrain_matrix(5, 30)

    final_map = twenty_gen_map[len(twenty_gen_map)-1]

    gen_img_from_map_matrix(final_map).show()
    save_terrain_history_gif(twenty_gen_map, (image_save_path+'LandSpreadTest10.gif'))

    test_cultures = []
    test_cultures.append(Culture(1, "The Shire", [250,10,10], False))
    test_cultures.append(Culture(2, "Mordor", [10,46,250], False))
    test_cultures.append(Culture(3, "Rohan", [255,234,0], False))
    test_cultures.append(Culture(4, "The Elves", [255,36,237], True))

    #TESTING CULTURE SPREAD
    test_culture_map = gen_culture_start_map(final_map, test_cultures)
    thirty_culture_spreads = generate_culture_matrix(final_map,test_cultures,200)
    final_culture_map = thirty_culture_spreads[0]
    Image.fromarray(get_culture_and_terrain_rgb(final_map,final_culture_map,test_cultures)).show()
    save_culture_history_gif(final_map,thirty_culture_spreads[1],test_cultures, (image_save_path+'NewCultureSpreadDemo4.gif'))


    #display_world_int(test_culture_map)
    #culture_rgb_map = get_culture_and_terrain_rgb(final_map, test_culture_map, test_cultures)

    #Image.fromarray((culture_rgb_map)).show()

    #print(test_culture_map.shape[0])



    #final_culture_map = thirty_culture_spreads[0]

    #display_world_int(final_culture_map)

    #Image.fromarray(get_culture_and_terrain_rgb(final_map,final_culture_map,test_cultures)).show()
    #save_culture_history_gif(final_map,thirty_culture_spreads[1],test_cultures, (image_save_path+'CultureSpreadDemo.gif'))

    #print(get_tile_ratios_for_cultures(final_map,final_culture_map,test_cultures))

    #TESTING FULLY RANDOM MAP GENERATION

    #start_map = gen_noise_map()
    #get_world_image(start_map).show()
    #twenty_gen_map = terrain_rule_iterations(start_map, 20)
    #get_world_image(twenty_gen_map[len(twenty_gen_map)-1]).show()
    #save_terrain_history_gif(twenty_gen_map, (image_save_path+'TestOutput.gif'))
