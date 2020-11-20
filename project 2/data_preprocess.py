import pandas as pd 
import numpy as np
import csv 


pd.set_option("display.max_columns",100)
df = pd.read_csv('Coffee-modified.csv')

# print(df.columns)

# df.drop(axis= 1, columns= ['Owner','Farm.Name','Mill','Company','Producer','Certification.Address','Certification.Contact'], inplace= True)


norm_cols = ['Species','Country.of.Origin','Number.of.Bags',"Bag.Weight","Harvest.Year","Variety","Processing.Method"]
flavor_cols = ["Aroma","Flavor","Aftertaste","Acidity","Body","Balance","Uniformity","Clean.Cup","Sweetness","Total.Cup.Points","Moisture","Category.One.Defects","Quakers","Category.Two.Defects","Certification.Body","altitude_low_meters","altitude_high_meters","altitude_mean_meters"]
cols = norm_cols + flavor_cols
print('column length: {}'.format(len(cols)))

df = df[cols]
# print(df.info())
# print(df.describe())

# print(df.loc[df['altitude_mean_meters']>3000])
print