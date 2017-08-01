
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
	columns = ['lng','lat']
	coordinates = pd.DataFrame(columns=columns) 
	index = 0
	# Create DataFrame with long and lat of pickup places
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
	# create distance_matrix for our points
	distance_matrix = squareform(pdist(coordinates, (lambda u,v: haversine(u,v))))
	# find clusters, need more word with parameters
	db = DBSCAN(eps=0.03, min_samples=1000, metric='precomputed') 
	y_db = db.fit_predict(distance_matrix)
	coordinates['cluster'] = y_db
	plt.scatter(coordinates['lat'], coordinates['lng'], c=coordinates['cluster'])
	df = pd.DataFrame([coordinates["lat"], coordinates["lng"], db.labels_]).T
	df.columns = ["lat","lng","cluster"]
	# write info about clusters centers(mean of long and lat) and number of members (for future ranking) 
	(df.groupby(["cluster"])['lat','lng'].mean()).to_csv("result_mean.csv")
	(df.groupby(["cluster"])['lat'].count()).to_csv("result_qua.csv")
`	# Save image to file
	plt.savefig('Clusters_NY_mirror.png')
	plt.show()



if __name__ == "__main__":
    main()
