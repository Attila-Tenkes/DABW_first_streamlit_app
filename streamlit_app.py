import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data(fruity_chioce):
  fruits = requests.get('https://fruityvice.com/api/fruit/'+ fruity_chioce)
  #streamlit.write('selected: ' , fruity_chioce)
  # streamlit.text(fruits.json())
  fruitVice_normalized = pandas.json_normalize(fruits.json())
  return fruitVice_normalized


def get_fruit_list():
  with my_cnx.cursor() as my_cur:
    # my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")  
    # my_data_row = my_cur.fetchone()
    my_data = my_cur.fetchall()
    my_cur.close()
    return my_data
  
def insert_to_spowflake(fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list (FRUIT_NAME) values ('" + fruit + "')")
    my_cur.close()
    return "Thanks for adding: " + fruit
    
    
    
streamlit.title('Fuit list content')
# get the file
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# set index colum
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header('FuityVice advice')
try:
  fruity_chioce = streamlit.text_input('What fruit would you like to get information about? ','kiwi')
  if not fruity_chioce:
    streamlit.error("Please select a fruit")
  else:    
    # call FruityVice API to load some data
    api_result = get_fruityvice_data(fruity_chioce)
    streamlit.dataframe(api_result)
except URLError as e:
  streamlit.error()



if streamlit.button("get the list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  rows = get_fruit_list()
  streamlit.text("List:")
  streamlit.dataframe(rows)

fruitToBeAdded = streamlit.text_input("What fruit would you like to add:")
if streamlit.button("add to the list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  res = insert_to_spowflake(fruitToBeAdded)
  streamlit.text(res)
  
  
#if fruitToBeAdded:
#  my_cur.execute("insert into  pc_rivery_db.public.fruit_load_list (FRUIT_NAME) values ('"+fruitToBeAdded+"')")


