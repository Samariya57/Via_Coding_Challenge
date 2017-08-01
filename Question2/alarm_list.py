import MySQLdb
import csv
from datetime import datetime

def main():
	format = '%Y-%m-%d %H:%M:%S'
	format_time = "%H:%M:%S"
	alarm_list = []
	drivers = {}
	input_date = "2013-04-09 15:00:00"
	week_days = {"Monday":"Sunday","Sunday":"Saturday","Saturday":"Friday", "Friday":"Thursday", "Thursday":"Wednesday", "Wednesday":"Tuesday", "Tuesday":"Monday"}
	db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="Via")
	cursor = db.cursor()
	update_stmt_95 = "Update {week_day} set count_95 = count_95+1 where id={minute}"
	update_stmt_10 = "Update {week_day} set count_10 = count_10+1 where id={minute}"
	for i in range(3,4,1):
		file = "sorted_data_"+str(i+1).zfill(2)+".csv" 
		with open(file, 'r') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			next(spamreader, None)
			for row in spamreader:
				if not (row[1] in drivers):
					listik = [row[6],row[5]]
					drivers[row[1]] = listik
				else:
					listik = drivers[row[1]]
					dif =  (datetime.strptime(row[5], format) - datetime.strptime(listik[0], format) )
					if dif.seconds > 3600: 
						on_shift_dif = (datetime.strptime(listik[0], format) - datetime.strptime(listik[1], format)).seconds // 60
						if on_shift_dif > 570:
							# we accept only drivers who crossed 9:40 threshold in less then 20 minutes before input date
							input_dif = (datetime.strptime(input_date,format) - datetime.strptime(listik[0], format) 
							if ((input_dif.seconds // 60) - on_shift_dif + 580) < 21:
								alarm_list.append(row[1] + " \n")
						listik[1] = row[5]
						listik[0] = row[6]
					else:
						listik[0] = row[6]
					drivers[row[1]] = listik
			file = open("alarm_list_20.txt","w")
			file.writelines(alarm_list)


if __name__ == "__main__":
    main()
