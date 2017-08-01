import MySQLdb
import csv
from datetime import datetime

def main():
	format = '%Y-%m-%d %H:%M:%S'
	format_time = "%H:%M:%S"
	drivers = {}
	#week_days = {"Monday":"Sunday","Sunday":"Saturday","Saturday":"Friday", "Friday":"Thursday", "Thursday":"Wednesday", "Wednesday":"Tuesday", "Tuesday":"Monday"}
	db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="Via")
	cursor = db.cursor()
	#update_stmt_95 = "Update {week_day} set count_95 = count_95+1 where id={minute}"
	#update_stmt_10 = "Update {week_day} set count_10 = count_95+1 where id={minute}"
	for i in range(12):
		file = "sorted_data_"+str(i+1).zfill(2)+".csv" 
		with open(file, 'r') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			next(spamreader, None)
			for row in spamreader:
				if not (row[1] in drivers):
					listik = [row[6],1, 0] # for each driver we store data about last drop-off, current on-roll length, and all times when he/she crossed 5 rides in a roll
					drivers[row[1]] = listik
				else:
					listik = drivers[row[1]]
					dif =  (datetime.strptime(row[5], format) - datetime.strptime(listik[0], format) )
					if dif.seconds < 600:
						listik[1] += 1
						if listik[1] == 5:
							listik[2] += 1
						listik[0] = row[6]
					else:
						listik[1] = 1
						listik[0] = row[6]
					drivers[row[1]] = listik
			print (len(drivers))
	# write data about on-roll times for each driver to db
	drivers_onroll_list = []
	for driver in drivers:
		drivers_onroll_list.append((driver,drivers[driver][2]))
	cursor.executemany("Insert Into ONROLL value (%s,%s)",drivers_onroll_list)
	db.commit()
if __name__ == "__main__":
    main()
