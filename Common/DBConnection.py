import os
import pymysql
import Common.Marker as Marker


class DBConnection:

    def __init__(self, hostname, password):
        """
        This class makes a connection with a mysql database called drones.
        If the database does not exist yet, a .sql script will run, make the database and fill it.
        Inside the database there are 2 tables: point and drone.

        point consist of entries with [id,x,y,z,transitpoint],
        each point corresponds to a physical arucomarker with an id and a x,y,z location.

        drone consist of entries with [id,x,y,z]
        each drone corresponds to a physical or simulated drone with an id and a x,y,z location.
        """
        try:
            self.db = pymysql.connect(
                host=hostname,
                user="root",
                password=password,
                db="drones"
            )
        except :
            # TODO: what is password or hostname is wrong
            print("make database")
            # database drones does not exist
            # so make it with the use of a .sql script
            self.db = pymysql.connect(
                host=hostname,
                user="root",
                password=password
            )
            cursor = self.db.cursor()
            # TODO: search for way to run sql sript at once command SOURCE does not work.
            # to be able to open this file from anywhere:
            # first take the absolute path to the current working directory
            # then split it
            # from there add SmartDrone\Common\init_DB.sql to get the full absolute path
            # note that this will only work if there is no other folder named SmartDrone
            # using os so this must work on any operating system
            path = os.path.join(os.getcwd().split("SmartDrone", 1)[0], "SmartDrone", "Common", "init_DB.sql").replace("\\" ,"/")
            for line in open(path, 'r').readlines():
                cursor.execute(line)

    def query(self, sql):
        """
        Make a query to the database
        :param: sql: the query
        :return: the answer from the database if the query was valid, "invalid query" otherwise
        """
        # run any command on the database

        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
            self.db.commit()
            return cursor.fetchall()
        except:
            return None

    def load_drones(self):
        drones = {}
        ids = {}
        try:
            for drone in self.query("select * from drones.drones"):
                ids[int(drone[2])] = drone[1]
                drones[drone[1]] = (drone[3], drone[4], drone[5])
        except Exception as e: print(e)
        return drones, ids

    def add_drone(self, id, unique_msg, location):
        x = location[0]
        y = location[1]
        z = location[2]
        try:
            self.query("insert into drones.drones(droneid, unique_msg, x,y,z) " +
                       "values(%d, %s, %d, %d, %d)" % (id, unique_msg, x, y, z))
        except Exception as e: print(e)

    def get_location(self, drone_id):
        location = (0,0,0)
        try:
            result = self.query("select x,y,z from drones.drones where droneID=%d" % drone_id)
            location = result[0]
        except Exception as e: print(e)
        return location

    def update_drone(self, id, location):
        x = float(location[0])
        y = float(location[1])
        z = float(location[2])
        try:
            query = "update drones.drones set x=%d, y=%d, z=%d where droneID=%d" % (x, y, z, id)
            self.query(query)
        except Exception as e: print(e)

    def remove_drone(self, drone_id, unique_msg):
        try:
            self.query("delete from drones.drones where droneID=%d and unique_msg=%s" % (drone_id, unique_msg))
        except Exception as e: print(e)

    def add_job(self, job):
        try:
            query = "insert into drones.jobs(droneID, active, start, stop, job_id) VALUES(%d, %d, %d, %d, %d)" % \
                    (-1, False,job["point1"], job["point2"], job["job_id"])
            self.query(query)
        except Exception as e: print(e)

    def remove_job(self, job_id):
        try:
            query = "delete from drones.jobs where job_id=%d" % job_id
            self.query(query)
        except Exception as e: print(e)

    def load_jobs(self):
        jobs = {}
        active_jobs = {}
        active_drones = []
        try:
            for job in self.query("select * from drones.jobs"):
                loaded_job = {
                    "point1": job[3],
                    "point2": job[4],
                    "job_id": job[5]
                }
                if int(job[2]) == 0:
                    jobs[int(job[5])] = loaded_job       # job not active, add job to job queue
                else:
                    active_drones.append(job[1])
                    active_jobs[int(job[5])] = loaded_job
        except Exception as e: print(e)
        return jobs, active_jobs, active_drones

    def set_job_active(self, job_id, drone_id):
        try:
            sql = "update drones.jobs set droneID=%d, active=%d where job_id=%d" % (drone_id, 1, job_id)
            self.query(sql)
        except Exception as e: print(e)

    def reset_job(self, job_id):
        try:
            sql = "update drones.jobs set droneID=%d, active=%d where job_id=%d" % (-1, 0, job_id)
            self.query(sql)
        except Exception as e: print(e)

    def get_markers(self):
        markers = {}
        for m in self.query("select * from drones.points"):
            marker = Marker.Marker(m[2], m[3], m[4], m[1])
            markers[m[1]] = marker
        return markers
