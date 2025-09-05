import streamlit as st
import pandas as pd
import request_spoon as rs
import os
from PIL import Image
from style import apply_styles 

st.title("Fridge Ingredients App")
apply_styles()  # apply styles before you render anything

def updatePageConfig():
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)
    os.chdir("..")
    icon = Image.open("assets/logo.png")
    st.set_page_config(page_title="Food Scanner", page_icon=icon, layout="wide")
    left, center, right = st.columns([1,1.5,1])
    center.image(icon)

def showByIngredients():
    """
    Search for recipes based on the ingredients entered by the user.
    Returns 2 recipes (Spoonacular's API (free tier) is limited to 50 points per day).
    """
    updateIngredientList()
    # Request recipes as long as at least one ingredient was entered
    if st.button("Get recipe(s)") and len(st.session_state["items"]) > 1:
        # Currently does not take amount into account
        items_as_list = [item["name"] for item in st.session_state["items"]]
        recipes = rs.requestRecipeByIngredients({"type": "main course"}, items_as_list)["results"]; # For now request 2 recipes due to spoonacular API tier limits
        printRecipes(recipes)

def updateIngredientList():
    if "items" not in st.session_state:
        st.session_state.items = [] # Holds the list of ingredients entered

    # Enter ingredients and add to list
    with st.form("ingredients_form"): 
        ingredient_name = st.text_input("Enter item name:").strip().lower()
        ingredient_amount = st.number_input("Enter the amount of the ingredient:",min_value=1, step=1, value=1)

        # subnit button
        submitted = st.form_submit_button("Add to list")
    if submitted:
        if ingredient_name in valid_input:
            if ingredient_name.strip():
                found = False
                for item in st.session_state["items"]:
                    if item["name"].lower() == ingredient_name.strip().lower():
                        item["amount"] += ingredient_amount
                        found = True
                        break
                    
                # Ingredient was not found
                if not found:
                    st.session_state["items"].append({
                        "name": ingredient_name.strip().capitalize(),
                        "amount": ingredient_amount
                    })
                    
                st.success(f"Added: {ingredient_name.lower()}")
        else:
            st.error("❌ Input not found. Try again.")    

    # Increase / decrease amount of each ingredient
    if st.session_state["items"]:
        st.subheader("List of ingredients:")
        for item in st.session_state["items"]:
            col1, increase, decrease, delete = st.columns([2,1,1,1])
            col1.write(f"{item['name']}: {item['amount']}")

            if increase.button("➕", key=f"plus_{item['name']}"):
                item["amount"] += 1

            if decrease.button("➖", key=f"minus_{item['name']}"):
                if item["amount"] > 1:
                    item["amount"] -= 1
                else:
                    st.warning(f"{item['name']} can’t be less than 1")

            # Remove the ingredient from the list
            if delete.button("🗑️ Delete", key=f"delete_{item['name']}"):
                st.session_state["items"].remove(item)
                st.success(f"Deleted: {item['name']}")
                st.rerun() # Refresh UI after deletion

def showByNutrients():
    """
    Search for recipes based on the nutrients values entered by the user.
    returns 2 recipes (Spoonacular's API (free tier) is limited to 50 points per day).
    """
    st.subheader("Set your nutrients values to filter:")
    # the range of nutrients

    min_cal, max_cal = st.slider("Min to max calories", 0, 3500, (300, 600), 50)
    min_protein, max_protein = st.slider("Min to max protiens (g)", 0, 200, (0, 40), 5)
    min_carbs, max_carbs = st.slider("Min to max carbs (g)", 0, 400, (0, 50), 5)
    min_fat, max_fat = st.slider("Min to max fats (g)", 0, 100, (0, 20), 5)

    if min_protein >= max_protein or min_carbs >= max_carbs or min_cal >= max_cal or min_fat >= max_fat:
        st.error("Minimum nutrients must be less than maximum nutrients.")
    else:
        if st.button("Get recipe(s)"):
            recipes = rs.requestRecipeByNutrients({"type": "main course"}, min_carbs=min_carbs, max_carbs=max_carbs, min_protein=min_protein, max_protein=max_protein, min_calories=min_cal, max_calories=max_cal, min_fat=min_fat, max_fat=max_fat)["results"]
            printRecipes(recipes)

def printRecipes(recipes: dict):
    for recipe in recipes:
        # Summary
        st.title(recipe["title"])
        st.write("Source: " + recipe["sourceUrl"] + ", " + recipe["creditsText"])
        st.divider()
        left_, left, right, right_ = st.columns([1,3,2,1])
        left.markdown(recipe["summary"], unsafe_allow_html=True)
        right.image(recipe["image"])

        info, general, steps = st.columns([1,1,3])
                
        # List ingredients
        ingredients = recipe["nutrition"]["ingredients"]
        info.subheader("🧺 **Ingredients:**", divider=True)
        for ingredient in ingredients:
            info.write(ingredient["name"].capitalize() + ": " + str(ingredient["amount"]) + " " + ingredient["unit"])
                
        # Show nutrients and other general information
        general.subheader("🥣 **General information:**", divider=True)
        general.write("Vegetarian: " + str(recipe["vegetarian"]))
        general.write("Vegan: " + str(recipe["vegan"]))
        general.write("Gluten free: " + str(recipe["glutenFree"]))
        nutrients = recipe["nutrition"]["nutrients"]
        new = [x for x in recipe["nutrition"]["nutrients"] if x["name"] in ["Calories", "Fat", "Carbohydrates", "Protein"]] # Take only required nutrients
        for nutrient in new:
            general.write(nutrient["name"] + ": " + str(nutrient["amount"]) + " " + nutrient["unit"])
                
        # Show recipe instructions
        steps.subheader("👨‍🍳 **Steps:**", divider=True)
        instructions = recipe["analyzedInstructions"][0]["steps"]
        for instruction in instructions:
            steps.write("Step " + str(instruction["number"]) + " - " + instruction["step"])

updatePageConfig()
st.header("Food Scanner", divider=True)
search_options = st.selectbox("Choose search mode:", ["by ingredients", "by nutrients"])

# Display the fields depending on the search option
if search_options == "by ingredients":
    # check if the input is valid
    with open("src/valid_ingredients.txt", 'r') as f:
        valid_input = [line.strip().lower() for line in f]
    showByIngredients()
elif search_options == "by nutrients":
    showByNutrients()