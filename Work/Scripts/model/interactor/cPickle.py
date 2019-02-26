import os
import pickle

import pandas
os.chdir('C:/Users/ирбисик/Documents/PYTHON/ProductsViewer/Work/Data')

with open('db.pickle',"rb") as F:
	T=pickle.load(F)
