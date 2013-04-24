import dbms

db = dbms.Database()
db.insert_taken(1,100)
db.insert_taken(1,200)
db.insert_taken(1,300)

courses = db.find_taken(1)
print courses
