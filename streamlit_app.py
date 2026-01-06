# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize Your Smoothie :balloon:")
st.write("Choose the fruits you want in your custom smoothie.")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# -----------------------------
# SESSION HANDLING (FIX)
# -----------------------------
try:
    # Works ONLY inside Snowflake Streamlit
    session = get_active_session()
except:
    # Fallback for GitHub / local execution
    connection_parameters = {
        "account" : "BZNJCAL-DLB00315",
        "user" : "Avanindraa",
        "password" : "Allstargod12**",
        "role" : "SYSADMIN",
        "warehouse" : "COMPUTE_WH",
        "database" : "SMOOTHIES",
        "schema" : "PUBLIC",
        "client_session_keep_alive" : "true"
    }
    session = Session.builder.configs(connection_parameters).create()

# -----------------------------
# APP LOGIC (UNCHANGED)
# -----------------------------
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME")), col("SEARCH_ON"))

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe
)

if ingredients_list:
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")



