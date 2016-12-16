from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from http import cookies
from tickets import *
import random

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        tic = ticketsDB()
        if self.path.startswith("/tickets"):
            tickets = tic.getTickets()
            self.header200()
            self.wfile.write(bytes(tickets, "utf-8"))
        else:
            self.header404("It seems that this resource has been lost in the chocolate pipes. An Oompa Loompa will be dispatched promptly to recover the artifact.")

    def do_POST(self):
        self.load_cookie()
        tic = ticketsDB()
        if self.path.startswith("/tickets"):
            if("Cookie" in self.headers):
                self.header403("The Oompa Loompas have already received your ticket. Please try again tomorrow.")
            else:
                self.cookie["oompa"] = "loompa"
                length = self.header201()
                data, amount = self.parseInput(length)
                if amount > 6:
                    self.header404("Unable to add ticket.")
                    return
                token = random.randrange(0, 7)
                tic.addTicket(data, token)
        else:
            self.header404("It seems that this resource has been lost in the chocolate pipes. An Oompa Loompa will be dispatched promptly to recover the artifact.")

    def header200(self):
        #OK
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

    def header201(self):
        #created element
        self.send_response(201)
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_cookie()
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        length = int(self.headers['Content-Length'])
        return length

    def header403(self, error):
        #Forbidden
        self.send_response(403)
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_cookie()
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("<p>403 "+error+"</p>", "utf-8"))


    def header404(self, error):
        #error
        self.send_response(404)
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_cookie()
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<p>404 "+error+"</p>", "utf-8"))

    def parseInput(self, length):
        data = self.rfile.read(length).decode("utf-8")
        num = 0
        parsed = parse_qs(data)
        for key in parsed:
            num += 1
        return parsed, num

    def load_cookie(self):
        if "Cookie" in self.headers:
            print("cookie in headers")
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            print("No cookie in headers")
            self.cookie = cookies.SimpleCookie()

    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

def run():
        listen = ("127.0.0.1", 8080)
        server = HTTPServer(listen, MyServer)

        print("Listening......")
        server.serve_forever()

run()
