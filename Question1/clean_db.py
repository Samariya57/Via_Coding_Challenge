import MySQLdb

def main():
	db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="Via")
	week = ["Monday","Sunday","Saturday", "Friday", "Thursday", "Wednesday","Tuesday"]
	list = []
	for i in range(1440):
		list.append(((i+1),0,0))
	delete_stmt = "Delete from {week}"
	insert_stmt = "Insert Into {week} value (%s,%s,%s)"	
	cursor = db.cursor()
	for day in week:
		cursor.execute(delete_stmt.format(week=day))
		db.commit
		cursor.executemany(insert_stmt.format(week=day),list)
		db.commit
		

if __name__ == "__main__":
    main()



