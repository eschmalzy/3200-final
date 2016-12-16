import sqlite3
import json

class ticketsDB:

    def __init__(self):
        pass

    def parseDict(self,data):
        values = ["", "", "", "", "", ""]
        for key in data:
            if key == "name":
                values[0] = (data.get(key)[0])
            if key == "age":
                values[1] = int(data.get(key)[0])
            if key == "guest":
                values[2] = data.get(key)[0]
        return values

    def rowFactory(self, cursor, row):
        d = {}
        for idX, col in enumerate(cursor.description):
            d[col[0]] = row[idX]
        return d

    def getNewestTicket(self):
        connection = sqlite3.connect("tickets.db")
        connection.row_factory = self.rowFactory
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tickets WHERE id = (SELECT MAX(id)  FROM tickets)")
        rows = cursor.fetchall()
        connection.close()
        return json.dumps(rows)

    def getTickets(self):
        connection = sqlite3.connect("tickets.db")
        connection.row_factory = self.rowFactory
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tickets")
        rows = cursor.fetchall()
        connection.close()
        return json.dumps(rows)

    def addTicket(self, entryInfo, token):
        contactInfo = self.parseDict(entryInfo)
        connection = sqlite3.connect("tickets.db")
        connection.row_factory = self.rowFactory
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tickets (name,age,guest,token) VALUES (?,?,?,?)",(contactInfo[0],contactInfo[1],contactInfo[2],token))
        connection.commit()
        connection.close()
