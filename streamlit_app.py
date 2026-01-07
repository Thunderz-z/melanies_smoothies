# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import requests

st.title("Customize Your Smoothie :balloon:")
st.write("Choose the fruits you want in your custom smoothie.")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Session handling
try:
    session = get_active_session()
except:
    session = Session.builder.configs({
        "account": "BZNJCAL-DLB00315",
        "user": "Avanindraa",
        "password": "Allstargod12**",
        "role": "SYSADMIN",
        "warehouse": "COMPUTE_WH",
        "database": "SMOOTHIES",
        "schema": "PUBLIC",
        "client_session_keep_alive": "true"
    }).create()

# Pull fruit name + API-safe name
fruit_df = session.table("smoothies.public.fruit_options") \
    .select(col("FRUIT_NAME"), col("SEARCH_ON")) \
    .to_pandas()

# Multiselect uses GUI names
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_df["FRUIT_NAME"]
)

if ingredients_list:
    ingredients_string = ""

    for fruit in ingredients_list:
        ingredients_string += fruit + " "

        search_on=fruit_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        
        api_name = fruit_df.loc[
            fruit_df["FRUIT_NAME"] == fruit, "SEARCH_ON"
        ].values[0]

        st.subheader(f"{fruit} Nutrition Information")

        response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{api_name}"
        )

        st.dataframe(response.json(), use_container_width=True)

    insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    if st.button("Submit Order"):
        session.sql(insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")
