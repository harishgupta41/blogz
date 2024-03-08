# APIs for Blogs
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    database="harry",
    username="harry",
    password="dl3san3581"
)

cursor = mydb.cursor()

def loginAPI(username, password):
    return