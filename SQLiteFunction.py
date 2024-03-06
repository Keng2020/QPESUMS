import sqlite3
from sqlite3 import Error

def createConnection(dbFile):
    conn = None
    try:
        conn = sqlite3.connect(dbFile)
        return conn
    except Error as e:
        print(e)

    return conn


def createTable(conn, createTableSQL):
    """ create a table from the 'createTableSQL' statement
    :param conn: Connection object
    :param createTableSQL: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(createTableSQL)
    except Error as e:
        print(e)


def createTask(conn, task):
    """ create a new task
    :param conn:
    :param task:
    :return:
    """
    sql = ''' INSERT INTO Locations(location_id, X, Y) VALUES(?, ?, ?)'''
    cur = conn.cursor()
    cur.executemany(sql, task)
    conn.commit()


def insertIntoRainfall(conn, task, year):
    if int(year) >= 2006:
        sql = f''' INSERT INTO Rainfall{year}(location_id, dateTime, rainfallValue) VALUES(?, ?, ?)'''
        cur = conn.cursor()
        cur.executemany(sql, task)
        conn.commit()


def insertIntoMaxRainfall(conn, task):
    sql = f''' INSERT INTO MaxRainfalls(location_id, year, duration, maxRainfall) VALUES(?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.executemany(sql, task)
    conn.commit()


def selectSQL(conn, task):
    cur = conn.cursor()
    cur.execute(task)
    rows = cur.fetchall()
    return rows
