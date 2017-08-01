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
						#week_day = datetime.strptime(listik[0], format).strftime('%A')
						#minutes = (datetime.strptime(listik[0].split()[1], format_time) - datetime.strptime("0:00:00", format_time)).seconds // 60
						# here we are going to understand minutes where driver got 9.5 and 10 limits
						if on_shift_dif > 600:
							input_dif = (datetime.strptime(input_date,format) - datetime.strptime(listik[0], format) )
							#db_minute_10 = minutes - on_shift_dif + 600
							#db_minute_95 = db_minute_10 - 30
							if ((input_dif.seconds // 60) - on_shift_dif + 580) < 21:
								alarm_list.append(row[1] + " \n")
							#if (db_minute_95<1):
						#		week_day = week_days[week_day]
						#		db_minute_95 += 1440
						#	if (db_minute_10<1):
						#		week_day = week_days[week_day]
						#		db_minute_10 += 1440
						#	cursor.execute(update_stmt_95.format(week_day=week_day,minute=db_minute_95))
						#	cursor.execute(update_stmt_10.format(week_day=week_day,minute=db_minute_10))
							
														
						elif on_shift_dif > 570:		
						#	db_minute_95 = minutes - on_shift_dif + 570
							if ((input_dif.seconds // 60) - on_shift_dif + 580) < 21:
								alarm_list.append(row[1]+" \n")
						#	if db_minute_95<1:
						#		week_day = week_days[week_day]
						#		db_minute_95 += 1440
						#	cursor.execute(update_stmt_95.format(week_day=week_day,minute=db_minute_95))
						# save historic drivers behavior here 
						#db.commit()
						listik[1] = row[5]
						listik[0] = row[6]
					else:
						listik[0] = row[6]
					drivers[row[1]] = listik
			file = open("alarm_list_20.txt","w")
			file.writelines(alarm_list)


if __name__ == "__main__":
    main()
