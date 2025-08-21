import streamlit as st
import pandas as pd
import request_spoon as rs

st.title("Food Scanner")

if "items" not in st.session_state:
    st.session_state.items = []

# input fields
IngredientName = st.text_input("Enter item name:")
Ingredient_amount = st.number_input("Enter the amount of the ingredient:",min_value=1, step=1, value=1)
# a button the add the ingredient
if st.button("Add to list"):
    if IngredientName.strip():
        found = False
        for item in st.session_state["items"]:
            if item["name"].lower() == IngredientName.strip().lower():
                item["amount"] += Ingredient_amount
                found = True
                break
        
        if not found:
            st.session_state["items"].append({
                "name": IngredientName.strip(),
                "amount": Ingredient_amount
            })
        
        st.success(f"Added: {IngredientName}")

# options to increase or decrease or delete the amount of each ingredient

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

        if delete.button("🗑️ Delete", key=f"delete_{item['name']}"):
            st.session_state["items"].remove(item)
            st.success(f"Deleted: {item['name']}")
            st.rerun()  # refresh UI after deletion

# Request recipes as long as at least one ingredient was entered
if st.button("Get recipes") and len(st.session_state["items"]) > 1:
    # Currently does not take amount into account
    items_as_list = [item["name"] for item in st.session_state["items"]]
    recipes = rs.requestRecipeSteps(items_as_list, 2); # For now request 2 recipes due to spoonacular API tier limits
    info_col, steps_col = st.columns(2)
    # Print each recipe with info on the left and steps on the right
    for info, steps in recipes:
        info_col.write(info)
        steps_col.write(steps)