import random
import numpy as np


    # WATER = 1
    # GRASSLAND = 2
    # DESERT = 3
    # JUNGLE = 4
    # MOUNTAIN = 5
    # SNOW = 6


tileTypes = ["water", "grassland", "desert", "jungle", "mountain", "snow"] #for recipe title generator

#recipeCategories = ["soup", "stew", "curry", "bake", "smoothie"] #for recipe title generator

functionNumbers = [1, 2, 3]

ingredientAmounts = ["whole", "half", "quarter"]



#plantDictionary = {'letana': ['water', ['leaf', 'root', 'stem']],
#'minach': ['snow', ['bud', 'stem']], 'aspaelion': ['desert', ['bud', 'leaf']],
#'strawnach': ['grassland', ['bud', 'leaf', 'root']],
#'spiodil': ['water', ['bud', 'leaf', 'root']],
#'aspamary': ['mountain', ['leaf', 'stem']],
#'mushmary': ['mountain', ['leaf', 'stem']],
#'spituce': ['jungle', ['bud', 'leaf', 'stem']],
#'netgette': ['snow', ['bud', 'leaf']],
#'spigette': ['snow', ['bud', 'leaf', 'stem']],
#'metuce': ['grassland', ['bud', 'root', 'stem']],
#'dandato': ['jungle', ['leaf', 'root', 'stem']],
#'strawodil': ['snow', ['root', 'stem']],
#'strawlic': ['mountain', ['leaf', 'root', 'stem']],
#'netnach': ['mountain', ['bud', 'root']],
#'strawato': ['water', ['root', 'stem']],
#'mushragus': ['desert', ['leaf', 'stem']],
#'dandlic': ['jungle', ['leaf', 'stem']],
#'letelion': ['snow', ['bud', 'leaf']],
#'tomlon': ['jungle', ['bud', 'leaf']]}




def getTileName(tileId):

    if type(tileId) is int:
        return tileTypes[tileId-1] #Converts name to id, "water" -> 1,  "jungle" -> 2
    elif type(tileId) is str:
        return tileId

#produces soup recipe as a dictionary
def soupRecipe(plantDictionary, ingredientAmounts, tileRatios):

    #find two most predominant tile types
    sortedValues = sorted(tileRatios, key=tileRatios.get, reverse=True)
    #print(sortedValues)
    mostCommonTileType = getTileName(sortedValues[0])
    #print(mostCommonTileType)
    secondMostCommonTileType = getTileName(sortedValues[1])
    #print(secondMostCommonTileType)

    #find plants from dictionary with those tile types
    plantsToUse = []
    for plant in plantDictionary:
        value = plantDictionary.get(plant)
        tileName = value[0]


        print(tileName, mostCommonTileType, secondMostCommonTileType, value)
        if(tileName == mostCommonTileType or tileName == secondMostCommonTileType):
            plantsToUse.append(plant)

    random.shuffle(plantsToUse)
    print("plantsToUse = ",plantsToUse)

    ingredients = getIngredients(plantsToUse, plantDictionary)
    print("ingredients = ",ingredients)

    ingredientsList_a = getStepsSoup(ingredients)
    ingredientsList_b = ingredientsList_a[1]
    #print(ingredientsList_b)

    steps_a = getStepsSoup(ingredients)
    steps_b = steps_a[0]

    recipe = {"ingredients": ingredientsList_b,
    "recipe category": "Soup",
    "recipe steps": steps_b,
    "prep time": getPrepTime(),
    "cook time": getCookTime(), "commonTileTypes":[mostCommonTileType, secondMostCommonTileType]}

    #print("final recipe:", recipe)

    return recipe

#helperMethod to create steps to make soup from ingredients
def getStepsSoup(ingredients):

    print(ingredients)

    ingredient1 = ingredients[0][0]
    ingredient2 = ingredients[0][1]
    ingredient3 = ingredients[0][2]

    ing1 = ingredients[1][0] + " " + ingredients[2][0] + " of " + ingredients[0][0]
    ing2 = ingredients[1][1] + " " + ingredients[2][1] + " of " + ingredients[0][1]
    ing3 = ingredients[1][2] + " " + ingredients[2][2] + " of " + ingredients[0][2]

    ingredientsList = [ing1, ing2, ing3]
    #print("ingredients list ", ingredientsList)

    stepOne = "Boil the " + ingredient1 + " and the " + ingredient2
    stepTwo = "Blend the cooked " + ingredient1 + " and the " + ingredient2
    stepThree = "Serve with a sprinkle of " + ingredient3

    stepsAndIngredientsList = [[stepOne, stepTwo, stepThree], ingredientsList]

    return stepsAndIngredientsList








#produces soup recipe as a dictionary
def smoothieRecipe(plantDictionary, ingredientAmounts, tileRatios):

    #find two most predominant tile types
    sortedValues = sorted(tileRatios, key=tileRatios.get, reverse=True)
    #print(sortedValues)
    mostCommonTileType = getTileName(sortedValues[0])
    #print(mostCommonTileType)
    secondMostCommonTileType = getTileName(sortedValues[1])
    #print(secondMostCommonTileType)

    #find plants from dictionary with those tile types
    plantsToUse = []
    for plant in plantDictionary:
        value = plantDictionary.get(plant)
        tile = value[0]
        if(tile == mostCommonTileType or tile == secondMostCommonTileType):
            plantsToUse.append(plant)
    #print(plantsToUse)

    ingredients = getIngredients(plantsToUse, plantDictionary)
    ingredientsList_a = getStepsSmoothie(ingredients)
    ingredientsList_b = ingredientsList_a[1]
    #print(ingredientsList_b)

    steps_a = getStepsSmoothie(ingredients)
    steps_b = steps_a[0]

    recipe = {"ingredients": ingredientsList_b,
    "recipe category": "Smoothie",
    "recipe steps": steps_b,
    "prep time": getPrepTime(),
    "cook time": getCookTime(), "commonTileTypes":[mostCommonTileType, secondMostCommonTileType]}

    #print("final recipe:", recipe)

    return recipe

#helperMethod to create steps to make soup from ingredients
def getStepsSmoothie(ingredients):

    ingredient1 = ingredients[0][0]
    ingredient2 = ingredients[0][1]
    ingredient3 = ingredients[0][2]
    ingredient4 = ingredients[0][3]
    ingredient5 = ingredients[0][4]

    ing1 = ingredients[1][0] + " " + ingredients[2][0] + " of " + ingredients[0][0]
    ing2 = ingredients[1][1] + " " + ingredients[2][1] + " of " + ingredients[0][1]
    ing3 = ingredients[1][2] + " " + ingredients[2][2] + " of " + ingredients[0][2]
    ing4 = ingredients[1][3] + " " + ingredients[2][3] + " of " + ingredients[0][3]
    ing5 = ingredients[1][4] + " " + ingredients[2][4] + " of " + ingredients[0][4]

    stepOne = "Blend the " + ingredient1 + " and the " + ingredient2 + " in a blender"
    stepTwo = "Add a teaspoon of raw " + ingredient3 + " to taste"
    stepThree = "Serve with a dash of " + ingredient4 + " cream in a tall glass with a straw, umbrella and slice of " + ingredient5

    ingredientsList = [ing1, ing2, ing3, ing4, ing5]
    #print("ingredients list ", ingredientsList)

    stepsAndIngredientsList = [[stepOne, stepTwo, stepThree], ingredientsList]

    return stepsAndIngredientsList








#produces stew recipe as a dictionary
def stewRecipe(plantDictionary, ingredientAmounts, tileRatios):

     #find two most predominant tile types
    sortedValues = sorted(tileRatios, key=tileRatios.get, reverse=True)
    #print(sortedValues)
    mostCommonTileType = getTileName(sortedValues[0])
    #print(mostCommonTileType)
    secondMostCommonTileType = getTileName(sortedValues[1])
    #print(secondMostCommonTileType)

    #find plants from dictionary with those tile types
    plantsToUse = []
    for plant in plantDictionary:
        value = plantDictionary.get(plant)
        tile = value[0]
        if(tile == mostCommonTileType or tile == secondMostCommonTileType):
            plantsToUse.append(plant)
    #print(plantsToUse)

    ingredients = getIngredients(plantsToUse, plantDictionary)
    ingredientsList_a = getStepsStew(ingredients)
    ingredientsList_b = ingredientsList_a[1]
    #print(ingredientsList_b)

    steps_a = getStepsStew(ingredients)
    steps_b = steps_a[0]

    recipe = {"ingredients": ingredientsList_b,
    "recipe category": "Stew",
    "recipe steps": steps_b,
    "prep time": getPrepTime(),
    "cook time": getCookTime(), "commonTileTypes":[mostCommonTileType, secondMostCommonTileType]}

    #print("final recipe:", recipe)

    return recipe

#helperMethod to create steps to make soup from ingredients
def getStepsStew(ingredients):

    ingredient1 = ingredients[0][0]
    ingredient2 = ingredients[0][1]
    ingredient3 = ingredients[0][2]
    ingredient4 = ingredients[0][3]
    ingredient5 = ingredients[0][4]

    ing1 = ingredients[1][0] + " of a " + ingredients[2][0] + " of a " + ingredients[0][0]
    ing2 = ingredients[1][1] + " of a " + ingredients[2][1] + " of a " + ingredients[0][1]
    ing3 = ingredients[1][2] + " of a " + ingredients[2][2] + " of a " + ingredients[0][2]
    ing4 = ingredients[1][3] + " of a " + ingredients[2][3] + " of a " + ingredients[0][3]
    ing5 = ingredients[1][4] + " of a " + ingredients[2][4] + " of a " + ingredients[0][4]

    ingredientsList = [ing1, ing2, ing3, ing4, ing5]
    #print("ingredients list ", ingredientsList)

    stepOne = "Cut the " + ingredient1 + ", " + ingredient2 + " and " + ingredient3 + " in to cubes"
    stepTwo = "Fry the " + ingredient4 + " for a few minutes, and then add the chopped " + ingredient1 + ", " + ingredient2 + " and " + ingredient3
    stepThree = " Add broth of " + ingredient4 + " and leave to simmer until tender "
    stepFour = "Once the " + ingredient1 + " is cooked through, serve with a side of " + ingredient5 + " bread"

    stepsAndIngredientsList = [[stepOne, stepTwo, stepThree, stepFour], ingredientsList]

    return stepsAndIngredientsList



#helper methods

#add lists and randomly choose from them for sections of recipe templates

#helperMethod to get ingredients for recipe
def getIngredients(plants,plantDictionary):

    ingredients =[[],[],[]]

    #for i in range(1, 10):
    for plant in plants:
        current_plant = plantDictionary.get(plant)
        #print("current plant:", current_plant)
        ingredients[0].append(plant)
        ingredients[1].append(random.choice(ingredientAmounts))
        ingredients[2].append(random.choice(current_plant[1]))

        #print("ingredients:", ingredients)

    return ingredients

#helperMethod to get prep time for recipe
def getPrepTime():

    possible_times = ["10","15","20","25","30"]

    return random.choice(possible_times)+" minutes"

#helperMethod to get cook time for rexcipe
def getCookTime():
    possible_times = ["< 15","20 - 30","60+"]
    return random.choice(possible_times)+" minutes"



#Main method for soup recipe
#soupRecipe(plantDictionary, ingredientAmounts, tileTypeRatios)

#Main method for smoothie recipe
#smoothieRecipe(plantDictionary, ingredientAmounts, tileTypeRatios)

#Main method for stew recipe
#stewRecipe(plantDictionary, ingredientAmounts, tileTypeRatios)



#call this as Main Method, picks random recipe function to run
def pickRandomRecipe(plantDictionary, functionNumbers, tileTypeRatios):
    switch = {
        1: soupRecipe(plantDictionary, ingredientAmounts, tileTypeRatios),
        2: smoothieRecipe(plantDictionary, ingredientAmounts, tileTypeRatios),
        3: stewRecipe(plantDictionary, ingredientAmounts, tileTypeRatios)
    }
    output = switch.get(random.choice(functionNumbers))
    print(output)
    return output


if __name__ == "__main__":

    tileTypeRatios = {"water": 20, "jungle": 10, "snow": 5, "desert": 25, "mountain": 10, "grassland": 30}

    plantDictionary = {'daffroom': ['jungle', ['bud', 'root', 'stem']],
    'letroom': ['desert', ['leaf']],
    'dandmber': ['jungle', ['bud', 'root']],
    'spiragus': ['mountain', ['bud', 'stem']],
    'banato': ['snow', ['bud', 'root']],
    'dandtle': ['desert', ['leaf', 'stem']],
    'cucumt': ['grassland', ['bud', 'leaf', 'stem']],
    'cucuberry': ['grassland', ['bud']],
    'daffana': ['desert', ['bud', 'leaf', 'root']],
    'aspagette': ['jungle', ['bud', 'stem']],
    'member': ['mountain', ['bud', 'leaf', 'stem']],
    'dandana': ['water', ['bud', 'leaf']],
    'garnach': ['desert', ['root']],
    'garmary': ['grassland', ['leaf', 'root', 'stem']],
    'netato': ['water', ['bud', 'leaf', 'stem']],
    'spiroom': ['desert', ['root', 'stem']],
    'spint': ['water', ['bud', 'leaf']],
    'dafflon': ['grassland', ['leaf', 'root']],
    'meberry': ['desert', ['bud', 'stem']]}


    pickRandomRecipe(functionNumbers, tileTypeRatios)

#    randomly pick a nunber functionNumbers list
#    switch statement uses this randomly picked number for condition
#    corresponding function to number in switch cases is executed
#    add name to recipe
