import MySQLdb
import csv
from datetime import datetime

def main():
	format = '%Y-%m-%d %H:%M:%S'
	format_time = "%H:%M:%S"
	drivers = {}
	week_days = {"Monday":"Sunday","Sunday":"Saturday","Saturday":"Friday", "Friday":"Thursday", "Thursday":"Wednesday", "Wednesday":"Tuesday", "Tuesday":"Monday"}
	db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="Via")
	cursor = db.cursor()
	ave_gap = [10,1]
	ave_ride = [10,1]
	update_stmt_95 = "Update {week_day} set count_95 = count_95+1 where id={minute}"
	update_stmt_10 = "Update {week_day} set count_10 = count_10+1 where id={minute}"
	for i in range(12):
		file = "sorted_data_"+str(i+1).zfill(2)+".csv" 
		with open(file, 'r') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			next(spamreader, None)
			for row in spamreader:
				last_ride =  (datetime.strptime(row[6], format) - datetime.strptime(row[5], format) ).seconds // 60
				ave_ride[0] += last_ride
				ave_ride[1] += 1
				if not (row[1] in drivers):
					listik = [row[6],row[5]]
					drivers[row[1]] = listik
				else:
					listik = drivers[row[1]]
					dif =  (datetime.strptime(row[5], format) - datetime.strptime(listik[0], format) )
					if dif.seconds > 3600: 
						#on_shift_dif = (datetime.strptime(listik[0], format) - datetime.strptime(listik[1], format)).seconds // 60
						#week_day = datetime.strptime(listik[0], format).strftime('%A')
						#minutes = (datetime.strptime(listik[0].split()[1], format_time) - datetime.strptime("0:00:00", format_time)).seconds // 60
						# here we are going to understand minutes where driver got 9.5 and 10 limits
						
						# save historic drivers behavior here 
						
						listik[1] = row[5]
						listik[0] = row[6]
					else:
						last_gap = dif.seconds // 60
						ave_gap[0] += last_gap
						ave_gap[1] += 1 
						listik[0] = row[6]
					drivers[row[1]] = listik
			print(ave_ride[0]/ave_ride[1],ave_gap[0]/ave_gap[1])
			#print (len(drivers))


if __name__ == "__main__":
    main()
