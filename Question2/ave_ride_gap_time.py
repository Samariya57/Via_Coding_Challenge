import MySQLdb
import csv
from datetime import datetime

def main():
	format = '%Y-%m-%d %H:%M:%S'
	format_time = "%H:%M:%S"
	drivers = {}
	db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="Via")
	cursor = db.cursor()
	ave_gap = [10,1]
	ave_ride = [10,1]
	for i in range(12):
		file = "sorted_data_"+str(i+1).zfill(2)+".csv" 
		with open(file, 'r') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			next(spamreader, None)
			for row in spamreader:
				# for ave ride time we don't have to store any data, only count each ride from files
				last_ride =  (datetime.strptime(row[6], format) - datetime.strptime(row[5], format) ).seconds // 60
				ave_ride[0] += last_ride
				ave_ride[1] += 1
				# for average gap time we have store info about last drop-off for each driver and don't count gaps between different on-shift periods
				if not (row[1] in drivers):
					listik = [row[6],row[5]]
					drivers[row[1]] = listik
				else:
					listik = drivers[row[1]]
					dif =  (datetime.strptime(row[5], format) - datetime.strptime(listik[0], format) )
					if dif.seconds > 3600:
						listik[1] = row[5]
						listik[0] = row[6]
					else:
						last_gap = dif.seconds // 60
						ave_gap[0] += last_gap
						ave_gap[1] += 1 
						listik[0] = row[6]
					drivers[row[1]] = listik
			print(ave_ride[0]/ave_ride[1],ave_gap[0]/ave_gap[1])


if __name__ == "__main__":
    main()
