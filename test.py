import pandas as pd
import matplotlib as plt


df = pd.read_csv("/home/pythondev/projects/Webscraping-monitoring-/output.csv")
new_df = df.loc["Timespan":"Price", :]
print(new_df)
