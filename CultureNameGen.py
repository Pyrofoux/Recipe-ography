import data
import data.CountryCities

import random
from enum import Enum, IntEnum
import json

country_cities = data.CountryCities.country_cities


class Cuisine(Enum):
    German = 'German'
    English = 'English'
    French = 'French'
    Italian = 'Italian'
    Greek = 'Greek'
    Chinese = 'Chinese'
    Japanese = 'Japanese'
    Portuguese = 'Portuguese'
    Hungarian = 'Hungarian'
    Hawaiian = 'Hawaiian'
    American = 'American'
    Cuban = 'Cuban'
    Indian = 'Indian'
    Irish = 'Irish'
    Mexican = 'Mexican'
    Moroccan = 'Moroccan'
    Swedish = 'Swedish'
    Spanish = 'Spanish'
    Thai = 'Thai'


#'German', 'English', 'French', 'Italian', 'Greek', 'Chinese', 'Japanese', 'Portuguese', 'Hungarian', 'Hawaiian', 'American', 'Cuban', 'Indian', 'Irish', 'Mexican', 'Moroccan', 'Swedish', 'Thai'

# ALl the data we have

# all_language_style = ['German', 'English', 'French', 'Italian', 'Castillian', 'Ruthenian', 'Nordic', 'Greek', 'Roman', 'Finnic', 'Korean', 'Chinese', 'Japanese', 'Portuguese', 'Nahuatl', 'Hungarian', 'Turkish', 'Berber', 'Arabic', 'Inuit', 'Basque', 'Nigerian', 'Celtic', 'Mesopotamian', 'Iranian', 'Hawaiian', 'Karnataka', 'Quechua', 'Swahili', 'Vietnamese', 'Cantonese', 'Mongolian', 'Human Generic', 'Elven', 'Dark Elven', 'Dwarven', 'Goblin', 'Orc', 'Giant', 'Draconic', 'Arachnid', 'Serpents']
#
#
# all_cuisine_styles = ["American","Chinese","Cuban","English","French","German","Greek","Hawaiian","Hungarian","Indian","Irish","Italian","Japanese","Mexican","Moroccan","Portuguese","Spanish","Swedish","Thai"]

# Common values:
#common = ['German', 'English', 'French', 'Italian', 'Greek', 'Chinese', 'Japanese', 'Portuguese', 'Hungarian', 'Hawaiian']

# Missing values:
#missing = ['American', 'Cuban', 'Indian', 'Irish', 'Mexican', 'Moroccan', 'Swedish', 'Thai']

# Thoughts on brdging some gaps:
# We could take Arabic for Morroco
# Nahuatl is the language spoken in old Mexico, but Mexico speaks mainly spanish
# Thai and Vietnamese are different languages!
# They speak Spanish in Cuba
# American => English
# Morroco => Arabic + Berber
# Mexican => Spanish + Nahuatl
# Thai => Vietnamese as its only for the region name
# Swedish => Nordic
# Irish => Celtic
# Indian => Karnataka

cuisine2language = {
    Cuisine.German: ['German'],
    Cuisine.English: ['English'],
    Cuisine.French: ['French'],
    Cuisine.Italian: ['Italian'],
    Cuisine.Greek: ['Greek'],
    Cuisine.Chinese: ['Chinese'],
    Cuisine.Japanese: ['Japanese'],
    Cuisine.Portuguese: ['Portuguese'],
    Cuisine.Hungarian: ['Hungarian'],
    Cuisine.Hawaiian: ['Hawaiian'],
    Cuisine.American:['English','Castillian'],
    Cuisine.Cuban:['Castillian'],
    Cuisine.Indian:['Karnataka'],
    Cuisine.Irish:['Celtic'],
    Cuisine.Mexican:['Nahuatl','Castillian'],
    Cuisine.Moroccan:['Arabic', 'Berber'],
    Cuisine.Swedish:['Nordic'],
    Cuisine.Spanish:['Castillian'],
    Cuisine.Thai:["Vietnamese"]
}


def vowel(letter):
    if letter in "aeiouy":
        return letter
    else:
        return ""

def capitalize(name):
    return name[0].upper()+name[1:].lower()

def syllablize(name, syllable_max_length = 3):

    name = name.lower()
    syllables = []

    i=-1
    syllable = ""
    while i < len(name):
        prev = name[i] or "" # pre-onset letter
        v = False # 0 if no vowels in syllable

        #c=i+1
        c=i
        while c < len(name)-1 and len(syllable) < syllable_max_length:
          c+=1
          that = name[c]

          syllable += that
          if syllable == " " or syllable == "-": break # syllable starts with space or hyphen

          if c+1 >= len(name): break

          next = name[c+1] # next char
          if next == " " or next == "-": break # no need to check

          if vowel(that): v = True # check if letter is vowel

          # do not split some diphthongs
          #diphtongs = ["oo","ee","ae","ch","ye","ou","ow","aw","ew",""]
          if that == "o" and next == "o": continue # 'oo'
          if that == "e" and next == "e": continue # 'ee'
          if that == "a" and next == "e": continue # 'ae'
          if that == "c" and next == "h": continue # 'ch'
          if that == "y" and next == "e": continue # 'ye'
          if that == "o" and next == "u": continue # 'ou'

          if vowel(that) == next:break # two same vowels in a row
          if v and c+2 < len(name) and vowel(name[c+2]):break # syllable has vowel and additional vowel is expected soon

        i += len(syllable) or 1
        syllables.append(syllable)
        syllable = ""


    return syllables[:-1]



def add2chain(chain, curr_syllable, next_syllable): #add a new syllable to the chain
    if curr_syllable not in chain: #initialize the structure if we haven't seen the syllables before
        chain[curr_syllable] = {}
    if next_syllable not in chain[curr_syllable]:
        chain[curr_syllable][next_syllable] = 0
    chain[curr_syllable][next_syllable] += 1
    return chain

def namebank2chain(namebank, syllable_max_length = 3): #creates a amrkov chain from a namebank
    #namebank = a list of names, like a country cities or most known recipe

    chain = {}

    for name in namebank: #Adding the transition states for each syllable
        name = name.lower()
        syllables = syllablize(name, syllable_max_length) #create syllables


        chain = add2chain(chain, "START", syllables[0])
        chain = add2chain(chain, syllables[-1], "END")

        for syllable_index in range(len(syllables)-1):
            curr_syllable = syllables[syllable_index]
            next_syllable = syllables[syllable_index+1]

            chain = add2chain(chain, curr_syllable, next_syllable)

    # Normalizing the chain
    for curr_syllable in chain:
        total = 0

        for next_syllable in chain[curr_syllable]:
            total += chain[curr_syllable][next_syllable]
        for next_syllable in chain[curr_syllable]:
            chain[curr_syllable][next_syllable] /= total

    return chain


def weighted_random_by_dct(dct):#gives a random possibility from a dictionary of probabilities
    rand_val = random.random()
    total = 0
    for k, v in dct.items():
        total += v
        if rand_val <= total:
            return k
    assert False, 'unreachable'


def chain2word(chain, n = 1): #generates a word from a markov chain

    word_list = []

    for i in range(n):
        current_state = "START"
        current_word = ""


        while current_state != "END":
            current_state = weighted_random_by_dct(chain[current_state])
            if current_state != "END":
                current_word += current_state
        word_list.append(current_word)

    if n == 1:
        return current_word
    else:
        return word_list


def cityNameFromCuisine(cuisine, force_new = True, min_length = 3, syllable_max_length = 3):

    name_bank = [] #Gathering the right languages
    for language in cuisine2language[cuisine]:
        name_bank += country_cities[language]["cities"]

    markov_chain = namebank2chain(name_bank, syllable_max_length) #Building the Markov chain

    #Generating a word:
    word = chain2word(markov_chain)
    if force_new or min_length > 0:
        max_attemps = 100
        while (capitalize(word) in name_bank or min_length > len(word)) and max_attemps > 0:
            max_attemps -= 1
            word = chain2word(markov_chain)

    return word

def recipeNameFromCuisine(cuisine,  force_new = True, min_length = 4,  syllable_max_length = 3):
        name_bank = getExistingRecipesNames(cuisine) #Gathering the right recipenames

        markov_chain = namebank2chain(name_bank,  syllable_max_length) #Building the Markov chain

        #Generating a word:
        word = chain2word(markov_chain)
        if force_new or min_length > 0:
            max_attemps = 100
            while (capitalize(word) in name_bank or min_length > len(word)) and max_attemps > 0:
                max_attemps -= 1
                word = chain2word(markov_chain)

        return word

def getExistingRecipesNames(cuisine):

    #Load the right JSON file
    filename = f"./data/country_dish_list/results_{cuisine.value.lower()}_Main Dishes.json"

    with open(filename, encoding="utf-8") as file:
        file = open(filename,'r', encoding="utf-8")
        decoded = str(file.read()).encode().decode('utf-8',"ignore")
        parsed = json.loads(decoded)
        file.close()

    recipes = parsed["matches"]
    recipeNames = []
    for recipe in recipes:

        #TODO: clean recipe name
        #emove brackets
        #remove mention of country
        #remove mention of ingredient???

        recipeNames.append(str(recipe["recipeName"].encode("utf-8")))
    return recipeNames


# This line says that everything after will only be executed if you run the script directly,
# and will not be run if you load the script from another module, like the Assembler :)
if __name__ == "__main__":
    #Generative examples

    #City
    print(capitalize(cityNameFromCuisine(Cuisine.Moroccan)))
    print(capitalize(cityNameFromCuisine(Cuisine.English)))
    print(capitalize(cityNameFromCuisine(Cuisine.French)))
    print(capitalize(cityNameFromCuisine(Cuisine.German)))
    print(capitalize(cityNameFromCuisine(Cuisine.Japanese)))

    #Recipe name
    print(recipeNameFromCuisine(Cuisine.French, syllable_max_length = 1))
