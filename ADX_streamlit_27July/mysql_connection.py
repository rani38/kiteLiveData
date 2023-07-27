import mysql.connector

hostname = 'localhost'
username = 'root'
password = ''
database = 'test'


def connection():
    try:
        myConnection = mysql.connector.connect( host=hostname, user=username, passwd=password, db=database )
        cur = myConnection.cursor()

        if myConnection:
            print("connection established")
            return myConnection,cur

    except:
        print("wrong credentials")
