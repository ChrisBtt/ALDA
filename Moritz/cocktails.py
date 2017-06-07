#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 16:54:17 2017

@author: moritzalthaus
"""


import json
import time
from itertools import combinations

recipes = json.load(open('cocktails.json', encoding = 'utf_8'))

def list_cocktails(inverse_recipes):
    '''Erstelle eine Liste aller Cocktails'''
    cocktails = []
    for ingredient in inverse_recipes:
        for cocktail in inverse_recipes[ingredient]:
            if cocktail not in cocktails:
                cocktails.append(cocktail)
    return cocktails

def list_ingredients(inverse_recipes):
    '''Erstelle eine Liste aller Ingredients'''
    ingredients = []
    for ingredient in inverse_recipes:
        ingredients.append(ingredient)
    return ingredients


'''Funktion gibt eine Liste von Cocktails zurück, die mit den
    gegebene Zutaten möglich ist, leer wenn kein möglicher Cocktail.
    Unwichtige Zutaten werden ignoriert: ignore_list'''
def possible_cocktails(inverse_recipes, available_ingredients):
    ignore_list = ["wasser", "salz", "pfeffer", "zucker", "eiswürfel", "crushed"]
    #ignore_list = [normalizeString(element) for element in ignore_list]
    
    '''Erstelle eine Liste aller Cocktails'''
    possible_cocktails = list_cocktails(inverse_recipes)
                
    '''Cocktails die nicht möglich sind, entfernen'''
    for ingredient in inverse_recipes:
        
        if ingredient not in available_ingredients  and ingredient not in ignore_list:
            for cocktail in inverse_recipes[ingredient]:
                if cocktail in possible_cocktails:
                    possible_cocktails.remove(cocktail)

    return possible_cocktails



"""Diese Funktion wird in optimal_ingredients aufgerufen und löscht in jeder
Schleife alle Cocktails aus inverse_recipe, die mit den i Zutaten, egal in
welcher Unterkombination, sowieso nicht möglich sind. So werden in der häufig
aufgerufenen Schleife Vergleiche gespart"""
def optimize_inverse_recipes(inverse_recipes, limited_ingredients):
    cocktails = possible_cocktails(inverse_recipes, limited_ingredients)
    for ingredient in inverse_recipes:
        for cocktail in inverse_recipes[ingredient]:
            if cocktail not in cocktails:
                inverse_recipes[ingredient].remove(cocktail)
    return inverse_recipes
            


def optimal_ingredients(inverse_recipes): 
    """Wir definieren einen Index i, der mit den 5 häufigsten Ingredients anfängt,
     und immer ein weiteres dazunimmt und alle Kombinationen testet. 
    und lassen eine Optimierung durchlaufen, bis der Algorithmus
    automatisch irgendwann abbricht"""
    ignore_list = ["wasser", "salz", "pfeffer", "zucker", "eiswürfel", "crushed"]
    timeout = 1000
    timeout_start = time.time()
    ingredients = list_ingredients(inverse_recipes)
    for element in ignore_list:
        ingredients.remove(element)
    optimal_ingredients = []

    number_of_cocktails = 0
    for length in range(5, len(ingredients)): #äußerste Schleife
        print("Länge: %s" %length)
        opt_inverse_recipes = optimize_inverse_recipes(inverse_recipes, ingredients[0: length])
        possible_combinations = combinations(ingredients[0: length], 5) 
        
        for combination in possible_combinations:
            number = len(possible_cocktails(opt_inverse_recipes, combination))
            if number > number_of_cocktails:
                number_of_cocktails = number
                optimal_ingredients = combination
            if time.time() > timeout_start + timeout:
                print("Anzahl der Cocktails: %s" %number_of_cocktails)
                return optimal_ingredients
  

    return optimal_ingredients




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

# print('Anzahl verschiedener Zutaten: {count}'.format(count = len(all_ingredients(recipes)[0])))

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
        # print(el[-1], "\n", ingredients[el[-1]])
        
        new_ingredients.append(ingredients[el[-1]])
        el = el.pop(-1) # delete index
    
    dic = dict(zip(new_ingredients, cocktails))
    return dic

# Anmerkung: Die Reihenfolge im Dictionary sollte die Richtige sein, irgendwie stimmt sie im entstehenden Json nicht

with open('cocktail_inverse.json', 'w', encoding = 'utf_8') as f:
    json.dump(cocktails_inverse(recipes), f, indent=4, separators=(',', ': '), ensure_ascii=False)
    
inverse_recipes = cocktails_inverse(recipes)

available_ingredients = ["crushed", "maracujasaft", "cognac", "maracujasirup", "orangensaft", "kokossirup"]
Cocktails = possible_cocktails(inverse_recipes, available_ingredients)
print(Cocktails)

print(optimal_ingredients(inverse_recipes))
























