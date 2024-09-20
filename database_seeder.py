import sqlite3


connection = sqlite3.connect("playground.db")

cursor = connection.cursor()

cursor.execute("create table users (id integer, first_name text, last_name text, email text, phone text, street_address text, city text, state text, zip text)")
cursor.execute("create table company (id integer, name text, email text)")

users = [
	(1, "John", "Doe", "john.doe@gmail.com", "555555555", "321 s willow road", "Normal", "IL", "38239"),
	(2, "Sam", "Poe", "Sam.Poe@gmail.com", "223453454", "2345 w maple ave", "Odd", "UT", "34565"),
	(3, "Matt", "Loe", "Matt.Loe@gmail.com", "555555555", "253 n maple road", "Harriman", "NA", "89723"),
	(4, "Gloria", "Roe", "Gloria.Roe@gmail.com", "345345354", "987 e cedar ave", "Detroit", "NY", "92344"),
	(5, "Samantha", "Dae", "Samantha.Dae@gmail.com", "555555555", "612 s maple ave", "Chicago", "CO", "12389"),
	(6, "Blake", "Doe", "Blake.Doe@gmail.com", "345345345", "2553 e pine street", "Vermont", "FL", "23450"),
	(7, "Sam", "Doe", "Sam.doe@gmail.com", "555555555", "345 s maple ave", "Boise", "UT", "23823"),
	(8, "Steven", "Dawson", "Steven.Dawson@gmail.com", "345345345", "5784 w pine street", "Vernel", "UT", "38349"),
	(9, "Steven", "Dawgson", "Steven.Dawgson@gmail.com", "555555555", "321 s apple ave", "Salt Lake City", "UT", "74757"),
	(10, "Dawson", "C", "Dawson.doe@gmail.com", "555555555", "25 w maple ave", "Pheonix", "AZ", "34984"),
	(11, "Victoria", "Doe", "Victoria.Doe@gmail.com", "555555555", "561 s Oak Crossing", "Lehi", "UT", "84043"),
	(12, "Roger", "Rabbit", "Roger.Rabbit@gmail.com", "234234534", "3489 w maple ave", "Gillete", "HI", "23489"),
	(13, "Harry", "Potter", "Harry.Potter@gmail.com", "555555555", "174 w maple stre", "St George", "AL", "29349"),
	(14, "John", "Doe", "John.doe@gmail.com", "234523454", "182 e maple ave", "Las Vegas", "NV", "66745"),
	(15, "John", "Doe", "john.doe@gmail.com", "555555555", "2383 s juniper ave", "Washington", "KT", "23458")
]

company = [
	(1, "Intelligence Inc", "brains@intelligence.com"),
	(2, "Money Lovers Inc", "pay_us@money.com"),
	(3, "Shark Tank LLC", "deep_pockets@sharks.com")
]

cursor.executemany("insert into users values(?, ?, ?, ?, ?, ?, ?, ?, ?)", users)
cursor.executemany("insert into company values(?, ?, ?)", company)

for row in cursor.execute('select * from users'):
	print(row)

connection.close()