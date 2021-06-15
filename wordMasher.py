import random
import numpy as np
from CultureNameGen import *



original_plants = ["dandelion", "spinach", "banana", "parsley", "courgette", "garlic","carrot","ananas","orange","pumpkin","radish",
"tomato", "strawberry", "melon", "cucumber", "mushroom", "rosemary", "mint", "lettuce", "asparagus", "nettle","potato","broccoli", "apple"]

edible_parts =["leaf", "stem", "bud", "root"]


# same order as the MapGeneration and the Web Viewer
tileTypes = ["water", "jungle", "snow", "desert", "mountain", "grassland"]

plantDictionary = {}



#function to make a new word (plant name) from two existing words
def wordMash(originalPlants):
  random_word_1 = random.choice(originalPlants)
  random_word_2 = random.choice(originalPlants)
  first_half = getFirstHalf(random_word_1)
  second_half = getSecondHalf(random_word_2)
  #check that the two random strings are different strings
  if(random_word_1 != random_word_2):
    mashedWord = first_half + second_half
    print(mashedWord)
    return (mashedWord,random_word_1, random_word_2)
  else:
      print("chose same word twice")
      wordMash(originalPlants)

#helper function to retrieve the first half of a word
def getFirstHalf(word):

    syllables = syllablize(word)
    firstHalf = syllables[:int(len(syllables)/2)]
    return "".join(firstHalf)

#helper function to retrieve the second half of a word
def getSecondHalf(word):
    syllables = syllablize(word)
    secondHalf = syllables[int(len(syllables)/2):]
    return "".join(secondHalf)

#def addTileTypePrefix(str, list):
    #tileTypes = ["water", "jungle", "snow", "desert", "mountain", "grassland"]
    #plant_name = random.choice(list) + " " + str
    #print(plant_name)
    #return plant_name

#addTileTypePrefix(wordMash(original_plants), tileTypes)


#data structure for recipes to retrieve data (dictionary)

#function to create a dictionary, with plant names as the keys, and tile type/edible plant parts
#associated with the key as the value
def create_plant_library(originalplants, tiletypes, edibles, max_plants = 15):
    plant_dictionary = {}
    mashup_list = make_keys_list(originalplants)

    #each biomes should have at least two plants growing there
    #or we will have issues when accessing some recipies ingredients
    forced_biomes = ["jungle", "snow", "desert", "mountain", "grassland"] * 3

    i = 0
    for parent_words in mashup_list:

        if i > max_plants:
            break

        if parent_words != None: #Why could it be none? That's a mystery!
            mashed_plant_name = parent_words[0]
            parent_A = parent_words[1]
            parent_B = parent_words[2]

            #/!\
            #This is where the edibles and tile types are attributed

            forced_biome = None
            if i < len(forced_biomes):
                forced_biome = forced_biomes[i]

            attributes_list = plant_attributes_as_list(tileTypes, edibles, forced_biome = forced_biome)
            attributes_list.append([parent_A, parent_B])

            plant_dictionary.update({mashed_plant_name : attributes_list})

        i+=1
    return plant_dictionary

#helper function to create a list of plant names to use as keys for the dictionary
def make_keys_list(originalplants):
    keysList = []
    for x in range(len(originalplants)):
        keysList.append(wordMash(originalplants))
    return keysList

#helper function to construct a list of edible parts to use as part of the value for a key in
#the plant dictionary
def plant_attributes_as_list(tileTypesList, ediblePartsList, forced_biome = None):
    edible_parts = [random.choice(ediblePartsList), random.choice(ediblePartsList), random.choice(ediblePartsList)]
    x = np.array(edible_parts)
    distinctEdibleParts = np.unique(x)
    converted = distinctEdibleParts.tolist()

    tile_type = random.choice(tileTypesList)
    if forced_biome != None:
        tile_type = forced_biome

    attributes = [tile_type, converted]
    #print("plant attributes are: ", attributes)
    return attributes

#create_plant_library(original_plants, tileTypes, edible_parts)


#function to remove any dictionary keys that are 'None' in the dictionary
def cleanUpDictionary(plantDictionary, orignialPlants):
    #print("initial keys:", plantDictionary)
    for x in plantDictionary:
        if(x == None or x == "None"):
           newKey = wordMash(original_plants)
           #print("replacement key: ", newKey)
           #replace 'None' with new key
           plantDictionary[newKey] = plantDictionary.pop(x)
    print("cleaned keys:", plantDictionary)
    return plantDictionary



# This line says that everything after will only be executed if you run the script directly,
# and will not be run if you load the script from another module, like the Assembler :)
if __name__ == "__main__":

    #Main method to run, will produce the plant dictinary
    cleanUpDictionary(create_plant_library(original_plants, tileTypes, edible_parts), original_plants)
