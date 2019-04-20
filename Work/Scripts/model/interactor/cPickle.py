import os
import pickle

import pandas
os.chdir('C:/Users/Tom/Documents/Python_projects/ProductsViewer/Work/Data')

with open('db.pickle',"rb") as F:
	T=pickle.load(F)
