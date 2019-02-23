import pickle
import os
os.chdir('C:/Users/ирбисик/Documents/PYTHON/ProductsViewer/Work/Data')

T=[]
with open('db.pickle','rb') as database:
	T=pickle.load(database)
