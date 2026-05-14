import os
import pandas as pd
from processKMLData import processKMLData

ROOT_DIR = os.path.join(os.getcwd().split('antartic')[0])
DATA_DIR = os.path.join(ROOT_DIR, *['2016'])
df = pd.DataFrame(columns=['Total Area'])
for filename in os.listdir(DATA_DIR):
    global total_area
    total_area = 0
    if filename.__contains__(".kmz"):
        print(os.path.join(DATA_DIR, filename))
        total_area = processKMLData(os.path.join(DATA_DIR, filename))
        print("AREA = {} Sq Km".format(total_area))
        df.loc[filename] = "{}".format(total_area)
        df.to_csv('total_area.csv')
