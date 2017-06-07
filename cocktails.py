#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

recipes = json.load(open('cocktails.json', encoding = 'utf_8'))

def all_ingredients(recipes):
    ingredients = []  # create new list with all normalized ingredients
    cocktails = []

    for name in recipes:  # loop over given cocktails as name
        for ingredient in recipes[name]["ingredients"]: # loop over each ingredient as ingredient
            normalized = normalizeString(ingredient)  # equalize strings to get a clear list
			     # append ingredient to final list, if not already in 
            try:
                if ingredients.index(normalized):
                    cocktails[ingredients.index(normalized)].append(name)
            except ValueError:
                ingredients.append(normalized)
                cocktails.append([name])

    return ingredients, cocktails

def normalizeString(s):

    s = s.partition(" ")[0].lower() # delete information behind space and lowercase
    s = s.partition("(")[0]
    if s[-1] == "," or s[-1] == "(":
        s = s[:-1]
    return s
# War für die alte Aufgabe
#print('Anzahl verschiedener Zutaten: {count}'.format(count = len(all_ingredients(recipes)[0])))

# creating inverse-dictionary
def cocktails_inverse(recipes):
    ingredients, cocktails = all_ingredients(recipes)
    # indexing cocktail lists
    i = 0
    for el in cocktails:
        el.append(i)
        i+=1
    # sorting cocktail list
    cocktails.sort(key=lambda x:len(x), reverse=True)
    new_ingredients = []
    for el in cocktails:
        new_ingredients.append(ingredients[el[-1]])
        el = el.pop(-1) # delete index
    
    dic = dict(zip(new_ingredients, cocktails))
    return dic

# Anmerkung: Die Reihenfolge im Dictionary sollte die Richtige sein, irgendwie stimmt sie im entstehenden Json nicht

with open('cocktail_inverse.json', 'w', encoding = 'utf_8') as f:
    json.dump(cocktails_inverse(recipes), f, indent=4, separators=(',', ': '), ensure_ascii=False)
    
###############################################################################

'''

Probleme, die es noch zu beheben gilt: - Elemente aus ignore_list müssen nicht zwingend enthalten sein
- nicht in Cocktails enthaltene Zutaten sollen übergeben werden dürfen

ignore_list = ['Wasser']

def possible_cocktails(inverse_recipes, available_ingredients):
    ingredients = available_ingredients
    ingredients.extend(ignore_list) # add not necessary ingredients to available ones
    ingredients = [normalizeString(cocktail) for cocktail in ingredients] # normailizing available ingredients
    
    # add for all ingredients cocktails that are possible to make
    cocktails = []
    for ingredient in ingredients:
        try:
            cocktails.extend(inverse_recipes[ingredient])
        except KeyError:
            continue
    # create list with availabe cocktails    
    new_cocktails = []   
    for cocktail in cocktails:
        # count ingredients of cocktail
        count = 0
        for ingredient in inverse_recipes:
            count = count + inverse_recipes[ingredient].count(cocktail)
        if cocktails.count(cocktail) == len(ingredients) and len(ingredients) == count: # every ingredients has to be in cocktail and no other ingredient has to in ingredient
            try:
                new_cocktails.index(cocktail)
            except: 
                new_cocktails.append(cocktail)
    return new_cocktails

cocktail_inverse = json.load(open('cocktail_inverse.json', encoding = 'utf_8'))

test = ['Zucker', 'wodka', 'Melone', 'Eiswürfel']

#print(cocktail_inverse['zitronensaft'])

print(possible_cocktails(cocktail_inverse, test))
            
'''   

def list_cocktails(inverse_recipes):
    '''Erstelle eine Liste aller Cocktails'''
    cocktails = []
    for ingredient in inverse_recipes:
        for cocktail in inverse_recipes[ingredient]:
            if cocktail not in cocktails:
                cocktails.append(cocktail)
    return cocktails
'''Funktion gibt eine Liste von Cocktails zurück, die mit den
    gegebene Zutaten möglich ist, leer wenn kein möglicher Cocktail.
    Unwichtige Zutaten werden ignoriert: ignore_list'''
def possible_cocktails(inverse_recipes, available_ingredients):
    ignore_list = ["wasser", "salz", "pfeffer"]
    
    ignore_list = [normalizeString(ingredient) for ingredient in ignore_list] # normailizing ignorableingredients
    iavailable_ingredients = [normalizeString(ingredient) for ingredient in available_ingredients] # normailizing available ingredients
    
    '''Erstelle eine Liste aller Cocktails'''
    possible_cocktails = list_cocktails(inverse_recipes)
                
    '''Cocktails die nicht möglich sind, entfernen'''
    for ingredient in inverse_recipes:
        
        if ingredient not in available_ingredients  and ingredient not in ignore_list:
            for cocktail in inverse_recipes[ingredient]:
                if cocktail in possible_cocktails:
                    possible_cocktails.remove(cocktail)

    return possible_cocktails
'''
Testing:
inverse_recipes = cocktails_inverse(recipes)
available_ingredients = ["crushed", "maracujasaft", "cognac", "maracujasirup", "orangensaft", "kokossirup"]
Cocktails = possible_cocktails(inverse_recipes, available_ingredients)
print(Cocktails)
'''

import itertools

test = [1,2,3]
stuff = [1, 2, 3]
for subset in itertools.combinations(stuff, 2):
    print(subset)