import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omeaga 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach, Rocket Smoothie')
streamlit.text('🐔 Hard Boiled Free-Range Eggs')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#set the index to be fruit name column.
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

# Display the table on the page.
#streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include and put it into a variable so selecte fruits can be displayed later
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

#Display only the selected values
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

#old way
#New function to display fruitvice api response
  #streamlit.header("Fruityvice Fruit Advice!")
  #fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  #streamlit.write('The user entered ', fruit_choice)
  #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  
  # take the json version and  Normalize the date
    #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Output in a table format using dataframe.
    #streamlit.dataframe(fruityvice_normalized)


#Create a repeatable code block (called a function)
def get_fruityvice_date(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
#Above old way in new organized way.  
#New function to display fruitvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error ("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_date(fruit_choice)
    streamlit.dataframe(back_from_function)
      
except URLError as e:
  streamlit.error()
  
streamlit.header("The fruit_load_list contains:")
#snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

#Add a button to load the fruit
if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
  

#Allow end user to add new fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("Insert into fruit_load_list values ('" + new_fruit + "')")
    return "Thanks for adding " + new_fruit
  
add_my_fruit = streamlit.text_input('What fruit would you like to add')  
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)
  
  
#put the stop so stremlit does not run anything after this statement
streamlit.stop()




#old way
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from fruit_load_list")
#my_data_rows = my_cur.fetchall()
#streamlit.header("The fruit_load_list contains:")
#streamlit.dataframe(my_data_rows)

#old way
#add_my_fruit = streamlit.text_input('What fruit would you like to add')

#streamlit.write('Thanks for adding', add_my_fruit)
#my_cur.execute("Insert into fruit_load_list values ('from streamlit')")
