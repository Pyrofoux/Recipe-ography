import random
import numpy as np



original_plants = ["dandelion", "spinach", "banana", "daffodil", "courgette", "garlic", 
"tomato", "strawberry", "melon", "cucumber", "mushroom", "rosemary", "mint", "lettuce", "asparagus", "nettle"]

edible_parts =["leaf", "stem", "bud", "root"]

tileTypes = ["water", "jungle", "snow", "desert", "mountain", "grassland"]

#plantDictionary = {'spimber': ['water',['leaf', 'stem']], 
 #                  'daffgette': ['snow',['leaf', 'root', 'stem']], 
  #                 'daffmary': ['water',['bud', 'stem']], 
   #                'strawmber': ['grassland',['bud', 'leaf', 'stem']],
    #                 None: ['grassland',['bud', 'leaf', 'stem']]}



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
    return mashedWord
  else:
      print("chose same word twice")
      wordMash(originalPlants)

#helper function to retrieve the first half of a word
def getFirstHalf(word):
   firstHalf = word[:len(word)/2]
   #print(firstHalf)
   return firstHalf

#helper function to retrieve the second half of a word
def getSecondHalf(word):
    secondHalf = word[len(word)/2:]
    #print(secondHalf)
    return secondHalf

#def addTileTypePrefix(str, list):
    #tileTypes = ["water", "jungle", "snow", "desert", "mountain", "grassland"]
    #plant_name = random.choice(list) + " " + str
    #print(plant_name)
    #return plant_name

#addTileTypePrefix(wordMash(original_plants), tileTypes)


#data structure for recipes to retrieve data (dictionary)

#function to create a dictionary, with plant names as the keys, and tile type/edible plant parts 
#associated with the key as the value
def create_plant_library(originalplants, tiletypes, edibles):
    plant_dictionary = {}
    key_list = make_keys_list(originalplants)
    for plant in key_list:
        plant_dictionary.update({plant : plant_attributes_as_list(tileTypes, edibles)})
    #print("plant dictionary: ", plant_dictionary)
    return plant_dictionary 

#helper function to create a list of plant names to use as keys for the dictionary
def make_keys_list(originalplants):
    keysList = []
    for x in range(20):
        keysList.append(wordMash(originalplants))
    return keysList

#helper function to construct a list of edible parts to use as part of the value for a key in 
#the plant dictionary
def plant_attributes_as_list(list1, list2):
    edible_parts = [random.choice(list2), random.choice(list2), random.choice(list2)]
    x = np.array(edible_parts)
    distinctEdibleParts = np.unique(x)
    converted = distinctEdibleParts.tolist()
    attributes = [random.choice(list1), converted]
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

#Main method to run, will produce the plant dictinary
cleanUpDictionary(create_plant_library(original_plants, tileTypes, edible_parts), original_plants)






  

