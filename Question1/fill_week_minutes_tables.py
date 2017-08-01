import MySQLdb
import csv
from datetime import datetime

def main():
	format = '%Y-%m-%d %H:%M:%S' # Format for day and time
	format_time = "%H:%M:%S"     # Format for only time
	drivers = {}		     # Dictionary with all drivers
	week_days = {"Monday":"Sunday","Sunday":"Saturday","Saturday":"Friday", "Friday":"Thursday", "Thursday":"Wednesday", "Wednesday":"Tuesday", "Tuesday":"Monday"}
	db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="Via")
	cursor = db.cursor()
	update_stmt_95 = "Update {week_day} set count_95 = count_95+1 where id={minute}"
	update_stmt_10 = "Update {week_day} set count_10 = count_10+1 where id={minute}"
	for i in range(12):
		file = "sorted_data_"+str(i+1).zfill(2)+".csv" 
		with open(file, 'r') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			next(spamreader, None)
			for row in spamreader:
				if not (row[1] in drivers):
					listik = [row[6],row[5]] # for each driver we store last drop-off time and begininng of his/her on-shift
					drivers[row[1]] = listik
				else:
					listik = drivers[row[1]]
					dif =  (datetime.strptime(row[5], format) - datetime.strptime(listik[0], format) )
					if dif.seconds > 3600: # If difference between current pickup and last drop-off more than hour 
						on_shift_dif = (datetime.strptime(listik[0], format) - datetime.strptime(listik[1], format)).seconds // 60
						week_day = datetime.strptime(listik[0], format).strftime('%A')
						minutes = (datetime.strptime(listik[0].split()[1], format_time) - datetime.strptime("0:00:00", format_time)).seconds // 60ime was
						# here we are going to understand minutes where driver got 9.5-hour and 10-hour thresholds
						if on_shift_dif > 600: #If on-shift time was > 10 hours
							db_minute_10 = minutes - on_shift_dif + 600
							db_minute_95 = db_minute_10 - 30
							if (db_minute_95<1): # edge case when we have to write to previous day table
								week_day = week_days[week_day]
								db_minute_95 += 1440
							if (db_minute_10<1): # edge case when we have to write to previous day table
								week_day = week_days[week_day]
								db_minute_10 += 1440
							cursor.execute(update_stmt_95.format(week_day=week_day,minute=db_minute_95))
							cursor.execute(update_stmt_10.format(week_day=week_day,minute=db_minute_10))
							
														
						elif on_shift_dif > 570: # if on-shift time was >9.5		
							db_minute_95 = minutes - on_shift_dif + 570
							if db_minute_95<1: # edge case when we have to write to previous day table
								week_day = week_days[week_day]
								db_minute_95 += 1440
							cursor.execute(update_stmt_95.format(week_day=week_day,minute=db_minute_95))
						# write a code to save historic drivers behavior here (in case) 
						db.commit()
						listik[1] = row[5] # new on-shift beginning
						listik[0] = row[6] # new last drop-off
					else:
						listik[0] = row[6] # new last drop-off
					drivers[row[1]] = listik
			print (len(drivers))


if __name__ == "__main__":
    main()
