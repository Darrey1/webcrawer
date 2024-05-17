import pandas as pd

df = pd.read_csv("/home/pythondev/projects/Webscraping-monitoring-/shoestore.csv")
ref = df['Title'].values
for data in ref:
    if str(data).lower() == str("Brooks Men's Ghost 16 - Blue Opal / Black / Nasturtiu").lower():
        print("found")
        break
        
    else:
        print("not found")



