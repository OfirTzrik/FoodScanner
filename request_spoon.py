import requests
import streamlit as st

def requestRecipeSteps(ingredients: list, number_of_recipes: int):
    """
    Return the information and steps of some n recipes
    Accepts the list of ingredients the user has and a number of recipes to retrieve
    Returned as a zip with each row being <information about the recipe, the recipe's steps>

    zip_object = requestRecipeSteps([list of ingredients as strings], how many recipes to get)
    for info, steps in zip_object:
        ...
    """
    # Request the recipes based on the ingredients passed
    ingredients_str = ",+".join(ingredients)
    request_parameters = {"ingredients": ingredients_str, "number": number_of_recipes,"apiKey": st.secrets["API_KEY"]}
    try:
        recipes = requests.get("https://api.spoonacular.com/recipes/findByIngredients", params=request_parameters).json()
    # This happens when the daily points limit has been reached (too many requests from spoonacular)
    except Exception as e:
        return None

    # Request the steps for each of the recipes received
    recipes_steps = []
    for recipe in recipes:
        url = "https://api.spoonacular.com/recipes/" + str(recipe["id"]) + "/analyzedInstructions"
        try:
            steps = requests.get(url, params=request_parameters).json()
        # This happens when the daily points limit has been reached (too many requests from spoonacular)
        except Exception as e:
            return None
        recipes_steps.append(steps)

    return zip(recipes, recipes_steps)

def requestRecipeByNutrients(min_carbs: int = 0, max_carbs: int = 500,
                             min_protein: int = 0, max_protein: int = 100,
                             min_calories: int = 0, max_calories: int = 5000,
                             min_fat: int = 0, max_fat: int = 150,
                             number_of_recipes: int = 2):
    """
    Return the information and steps of some n recipes
    Accepts nutrient information from the user and a number of recipes to retrieve
    Returned as a zip with each row being <information about the recipe, the recipe's steps>

    zip_object = requestRecipeSteps(..., ..., ..., how many recipes to get)
    for info, steps in zip_object:
        ...
    """
    request_parameters = {
        "minCarbs": min_carbs, "maxCarbs": max_carbs,
        "minProtein": min_protein, "maxProtein": max_protein,
        "minCalories": min_calories, "maxCalories": max_calories,
        "minFat": min_fat, "maxFat": max_fat,
        "number": number_of_recipes,
        "apiKey": st.secrets["API_KEY"]
    }
    # Request the recipes based on the nutrients passed
    try:
        recipes = requests.get("https://api.spoonacular.com/recipes/findByNutrients", params=request_parameters).json()
    # This happens when the daily points limit has been reached (too many requests from spoonacular)
    except Exception as e:
        return None
    
    # Request the steps for each of the recipes received
    recipes_steps = []
    for recipe in recipes:
        url = "https://api.spoonacular.com/recipes/" + str(recipe["id"]) + "/analyzedInstructions"
        try:
            steps = requests.get(url, params=request_parameters).json()
        # This happens when the daily points limit has been reached (too many requests from spoonacular)
        except Exception as e:
            return None
        recipes_steps.append(steps)

    return zip(recipes, recipes_steps)