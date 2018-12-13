import os
import pymysql


class DBConnection:

    def __init__(self):
        """
        This class makes a connection with a mysql database called drones.
        If the database does not exist yet, a .sql script will run, make the database and fill it.
        Inside the database there are 2 tables: point and drone.

        point consist of entries with [id,x,y,z,transitpoint],
        each point corresponds to a physical arucomarker with an id and a x,y,z location.

        drone consist of entries with [id,x,y,z]
        each drone corresponds to a physical or simulated drone with an id and a x,y,z location.
        """
        hostname = "smartcity.ddns.net"
        password = "smartcity"
        try:
            self.db = pymysql.connect(
                host=hostname,
                user="root",
                password=password,
                db="drones"
            )
        except :
            print("make database")
            # database drones does not exist
            # so make it with the use of a .sql script
            self.db = pymysql.connect(
                host=hostname,
                user="root",
                password=password
            )
            cursor = self.db.cursor()
            # TODO search for way to run sql sript at once command SOURCE does not work.
            # to be able to open this file from anywhere:
            # first take the absolute path to the current working directory
            # then split it
            # from there add SmartDrone\Common\init_DB.sql to get the full absolute path
            # note that this will only work if there is no other folder named SmartDrone
            # using os so this must work on any operating system
            path = os.path.join(os.getcwd().split("SmartDrone", 1)[0], "SmartDrone", "Common", "init_DB.sql").replace("\\" ,"/")
            for line in open(path, 'r').readlines():
                cursor.execute(line)

    def query(self, message):
        """
        Make a query to the database
        :param message: the query
        :return: the answer from the database if the query was valid, "invalid query" otherwise
        """
        # run any command on the database
        cursor = self.db.cursor()
        # check if query is valid
        try:
            cursor.execute(message)
            return cursor
        except pymysql.connector.errors.ProgrammingError:
            return "invalid query"

    def add_drone(self, id, location):
        """
        Adds a drone to the database
        :param id: id of drone
        :param location: location of drone
        """
        cursor = self.db.cursor()
        x = location[0]
        y = location[1]
        z = location[2]
        query = "insert into drone(droneid, x,y,z) values(" + str(id) + "," + str(x) + "," + str(y) + "," + str(z) + ")"
        cursor.execute(query)


if __name__ == "__main__":

    """
    Small test case for DBConnection
    """
    db = DBConnection()
    out = db.query("select * from point")
    for i in out:
        print(i)
