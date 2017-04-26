from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import psycopg2
import unirest
import json

columns = []

def rip():
	def get_data():
		#Retrieve data from API endpoint
		response = unirest.get("https://omgvamp-hearthstone-v1.p.mashape.com/cards/sets/Classic",
			headers={
					"X-Mashape-Key": "TRI1WfO8dumshQd3krFUgj9bRf2ep1x76TvjsnH28h6bhADgnw"
			})
		#Initialize Pandas dataframe
		cols = ["name", "class", "rarity", "cost", "attack", "health"]
		df = pd.DataFrame(columns=cols)
		#Store data in dataframe
		for i in range(0, len(response.body)):
			entry = response.body[i]
			#Only consider playable cards
			if "cost" not in entry:
				continue
			else:
				name = entry["name"]
				clss = entry["playerClass"]
				cost = entry["cost"]
				#Not all cards have rarity (default) or attack/health (spells)
				try:
					rarity = entry["rarity"]
					attack = entry["attack"]
					health = entry["health"]
				except:
					rarity = np.nan
					attack = np.nan
					health = np.nan
				df.loc[index] = [name, clss, rarity, cost, attack, health]

		return df

	#Store dataframe into PostgreSQL database
	def store(dataframe):
		engine = create_engine("postgresql://test:pass@localhost:5432/hearthquiz")
		dataframe.to_sql("classic", engine)

	df = get_data()
	print df
	#store(df)

sets = ["Classic"]
rip()