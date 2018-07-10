import os 
import sqlite3
import pandas as pd

con = sqlite3.connect('database.db')
df = pd.read_sql("SELECT * FROM Image", con=con)

for index, row in df.iterrows():
    type = row['type'].split('.')[-1]
    with open('./images/'+str(index) + '.'+str(type),'wb' ) as f:
        f.write(row['bin'])

