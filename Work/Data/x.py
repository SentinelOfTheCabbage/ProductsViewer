import pickle
with open(r"C:\Users\Tom\Documents\Python_projects\ProductsViewer\Work\Data\db.pickle","rb") as f:
	db = pickle.load(f)

print (db['_db_products'].iloc[0])