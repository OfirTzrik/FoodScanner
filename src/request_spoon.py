import streamlit as st
import requests as rs
import random as rnd

def requestRecipeByIngredients(general_params: dict, ingredients: list):
    """
    Given a list of ingredients, return recipes that involve at least one or more of the ingredients
    Accepts a dictionary for more filtration parameters such as dish type, diet, cuisine, etc
    """
    ingredients_str = {"includeIngredients": ",+".join(ingredients)}
    return makeSpoonacularRequest(general_params | ingredients_str)

def requestRecipeByNutrients(general_params: dict, min_carbs: int = 0, max_carbs: int = 400, min_protein: int = 0, max_protein: int = 200, min_calories: int = 0, max_calories: int = 3500, min_fat: int = 0, max_fat: int = 100):
    """
    Given a nutrient numbers, return recipes that are within the ranges
    Accepts a dictionary for more filtration parameters such as dish type, diet, cuisine, etc
    """
    nutrients = {"minCarbs": min_carbs, "maxCarbs": max_carbs, "minProtein": min_protein, "maxProtein": max_protein, "minCalories": min_calories, "maxCalories": max_calories, "minFat": min_fat, "maxFat": max_fat}
    return makeSpoonacularRequest(general_params | nutrients)

def makeSpoonacularRequest(request_parameters: dict):
    """
    Make the request to Spoonacular's API with the general parameters and ingredients / nutrients
    """
    req_params = request_parameters | {"number": 2,"addRecipeInformation": True, "addRecipeInstructions": True, "addRecipeNutrition": True, "sort": "max-used-ingredients", "apiKey": st.secrets["API_KEY"]}

    try:
        recipes = rs.get("https://api.spoonacular.com/recipes/complexSearch", params=req_params, timeout=5).json()
    # This happens when the daily points limit has been reached (too many requests from spoonacular)
    except Exception as e:
        return None
    
    return recipes