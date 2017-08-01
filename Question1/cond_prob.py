from __future__ import division
import MySQLdb
import csv
from datetime import datetime

# We don't use window slicing for culculations, because this script is one time job 
def main():
	format = '%Y-%m-%d %H:%M:%S'
	format_time = "%H:%M:%S"
	drivers = {}
	week_days_back = {"Monday":"Sunday","Sunday":"Saturday","Saturday":"Friday", "Friday":"Thursday", "Thursday":"Wednesday", "Wednesday":"Tuesday", "Tuesday":"Monday"}

	week_days_forward = {"Sunday":"Monday","Saturday":"Sunday","Friday":"Saturday", "Thursday":"Friday", "Wednesday":"Thursday", "Tuesday":"Wednesday", "Monday":"Tuesday"}
	db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="Via")
	cursor = db.cursor()
	sum_stmt_95 = "Select sum(count_95) from {week_day} where id<={minute_right} and id>={minute_left}"
	sum_stmt_10 = "Select sum(count_10) from {week_day} where id<={minute_right} and id>={minute_left}"
	insert_stmt = "Insert Into {week_day}_Prob value (%s,%s)"
	for day in week_days_back:
		for i in range(1440):
			if i<30:
				# if minute is <30 then we have to look at previous day table as well as current
				cursor.execute(sum_stmt_95.format(week_day=day,minute_left=1,minute_right=i+1))
				left_sum = int(cursor.fetchone()[0])
				cursor.execute(sum_stmt_95.format(week_day=week_days_back[day],minute_left=1411+i,minute_right=1440))
				left_sum += int(cursor.fetchone()[0]) 
				cursor.execute(sum_stmt_10.format(week_day=day,minute_left=i+1,minute_right=i+31))
				right_sum = int(cursor.fetchone()[0])
			elif i>1410:
				# if minute is >1410 then we have to look at next day table as well as current
				cursor.execute(sum_stmt_95.format(week_day=day,minute_left=i-29,minute_right=i+1))
				left_sum = int(cursor.fetchone()[0])
				cursor.execute(sum_stmt_10.format(week_day=day,minute_left=i+1,minute_right=1440))
				right_sum = int(cursor.fetchone()[0])
				cursor.execute(sum_stmt_10.format(week_day=week_days_forward[day],minute_left=1,minute_right=1469-i))
				right_sum += int(cursor.fetchone()[0])
			else:
				cursor.execute(sum_stmt_95.format(week_day=day,minute_left=i-29,minute_right=i+1))
				left_sum = int(cursor.fetchone()[0])
				cursor.execute(sum_stmt_10.format(week_day=day,minute_left=i+1,minute_right=i+31))
				right_sum = int(cursor.fetchone()[0])
			cursor.execute(insert_stmt.format(week_day=day),(i+1,"%.7f" % (right_sum/left_sum))))
			db.commit()	

if __name__ == "__main__":
    main()
