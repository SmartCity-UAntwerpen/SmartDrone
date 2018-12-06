import mysql.connector


class DBConnection:

    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="student",
                database="drones"
            )
        except:
            print("make database")
            # database drones does not exist
            # so make it with the use of a .sql script
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="student",
            )
            cursor = self.db.cursor()
            # TODO search for way to run sql sript at once command SOURCE does not work.
            for line in open('init_DB.sql', 'r').readlines():
                cursor.execute(line)

    def query(self, message):
        # run any command on the database
        cursor = self.db.cursor()
        # check if query is valid
        try:
            cursor.execute(message)
            return cursor
        except mysql.connector.errors.ProgrammingError:
            return "invalid query"

    def add_drone(self, id, location):
        cursor = self.db.cursor()
        x = location[0]
        y = location[1]
        z = location[2]
        query = "insert into drone(droneid, x,y,z) values(" + str(id) + "," + str(x) + "," + str(y) + "," + str(z) + ")"
        cursor.execute(query)


if __name__ == "__main__":

    db = DBConnection()
    out = db.query("select * from drone")
    for x in out:
        print(x)

    db.add_drone(1, [1, 2, 3])

    out = db.query("select * from drone")
    for x in out:
        print(x)
