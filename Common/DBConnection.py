import os
import pymysql


class DBConnection:

    def __init__(self):
        try:
            self.db = pymysql.connect(
                # host="smartcity.ddns.net:3306",
                host="localhost",
                user="root",
                password="student",
                # password="smartcity",
                db="drones"
            )
        except:
            print("make database")
            # database drones does not exist
            # so make it with the use of a .sql script
            self.db = pymysql.connect(
                # host="smartcity.ddns.net:3306",
                host="localhost",
                user="root",
                password="student"
                # assword="smartcity",
            )
            cursor = self.db.cursor()
            # TODO search for way to run sql sript at once command SOURCE does not work.
            # to be able to open this file from anywhere:
            # first take the absolute path to the current working directory
            # then split it
            # from there add SmartDrone\Common\init_DB.sql to get the full absolute path
            # note that this will only work if there is no other folder named SmartDrone
            # using os so this must work on any operatings system
            path = os.path.join(os.getcwd().split("SmartDrone", 1)[0], "SmartDrone", "Common", "init_DB.sql").replace("\\" ,"/")
            for line in open(path, 'r').readlines():
                cursor.execute(line)

    def query(self, message):
        # run any command on the database
        cursor = self.db.cursor()
        # check if query is valid
        try:
            cursor.execute(message)
            return cursor
        except pymysql.connector.errors.ProgrammingError:
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
    out = db.query("select * from point")
    for i in out:
        print(i)
