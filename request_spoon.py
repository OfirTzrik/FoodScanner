import requests
import streamlit as st

def requestRecipeSteps(recipes, request_parameters: dict) -> list:
    """
    Request the steps for some n recipes
    Accepts the list of ingredients and the request parameters needed
    Returns the list of steps for each recipe to the calling function
    """
    recipes_steps = []
    for recipe in recipes:
        url = f"https://api.spoonacular.com/recipes/{recipe["id"]}/analyzedInstructions"
        try:
            steps = requests.get(url, params=request_parameters).json()
        # This happens when the daily points limit has been reached (too many requests from spoonacular)
        except Exception as e:
            return None
        recipes_steps.append(steps)
    return recipes_steps

def requestRecipeByIngredients(ingredients: list, number_of_recipes: int):
    """
    Return the information and steps of some n recipes based on ingredients entered
    Accepts the list of ingredients the user has and a number of recipes to retrieve
    Returned as a zip with each row being <information about the recipe, the recipe's steps>
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
    recipes_steps = requestRecipeSteps(recipes, request_parameters)

    return zip(recipes, recipes_steps)

def requestRecipeByNutrients(min_carbs: int = 0, max_carbs: int = 500, min_protein: int = 0, max_protein: int = 100, min_calories: int = 0, max_calories: int = 5000, min_fat: int = 0, max_fat: int = 150, number_of_recipes: int = 2):
    """
    Return the information and steps of some n recipes based on nutrients entered
    Accepts nutrient information from the user and a number of recipes to retrieve
    Returned as a zip with each row being <information about the recipe, the recipe's steps>
    """
    request_parameters = {"minCarbs": min_carbs, "maxCarbs": max_carbs, "minProtein": min_protein, "maxProtein": max_protein, "minCalories": min_calories, "maxCalories": max_calories, "minFat": min_fat, "maxFat": max_fat, "number": number_of_recipes, "apiKey": st.secrets["API_KEY"]}
    # Request the recipes based on the nutrients passed
    try:
        recipes = requests.get("https://api.spoonacular.com/recipes/findByNutrients", params=request_parameters).json()
    # This happens when the daily points limit has been reached (too many requests from spoonacular)
    except Exception as e:
        return None
    
    # Request the steps for each of the recipes received
    recipes_steps = requestRecipeSteps(recipes, request_parameters)

    return zip(recipes, recipes_steps)

def requestRecipeInformation(recipe_id: int):
    """
    Get full information about a given recipe
    Used for getting a full list of ingredients when searching by nutrients
    """
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    try:
        return requests.get(url, params={"apiKey": st.secrets["API_KEY"]}).json()
    except Exception:
        return None