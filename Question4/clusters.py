
from math import radians, cos, sin, asin, sqrt
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import pandas as pd
import csv

def haversine(lonlat1, lonlat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lat1, lon1 = lonlat1
    lat2, lon2 = lonlat2
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def main():
	#format = '%Y-%m-%d %H:%M:%S'
	#format_time = "%H:%M:%S"
	#drivers = {}
	#week_days = {"Monday":"Sunday","Sunday":"Saturday","Saturday":"Friday", "Friday":"Thursday", "Thursday":"Wednesday", "Wednesday":"Tuesday", "Tuesday":"Monday"}
	#db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="Via")
	#cursor = db.cursor()
	#update_stmt_95 = "Update {week_day} set count_95 = count_95+1 where id={minute}"
	#update_stmt_10 = "Update {week_day} set count_10 = count_10+1 where id={minute}"
	columns = ['lng','lat']
	coordinates = pd.DataFrame(columns=columns) 
	index = 0
	for i in range(12):
		file = "sorted_data_"+str(i+1).zfill(2)+".csv" 
		with open(file, 'r') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			next(spamreader, None)
			for row in spamreader:
				lng = float(row[10])
				lat = float(row[11])
				if lng < -73  and lat > 40.5:
					coordinates.loc[len(coordinates)]=[lng,lat]
				if len(coordinates) > 10000:
					break
		print(len(coordinates))
		distance_matrix = squareform(pdist(coordinates, (lambda u,v: haversine(u,v))))
		db = DBSCAN(eps=0.03, min_samples=3, metric='precomputed') 
		y_db = db.fit_predict(distance_matrix)
		coordinates['cluster'] = y_db
		#print(coordinates)
		plt.scatter(coordinates['lat'], coordinates['lng'], c=coordinates['cluster'])
		df = pd.DataFrame([coordinates["lat"], coordinates["lng"], db.labels_]).T # Add other attributes of coordinates if needed
		df.columns = ["lat","lng","cluster"]
		(df.groupby(["cluster"])['lat','lng'].mean()).to_csv("result_mean.csv")
		(df.groupby(["cluster"])['lat'].count()).to_csv("result_qua.csv")
		#plt.show()
		plt.savefig('books_read.png')
		plt.show()



if __name__ == "__main__":
    main()
