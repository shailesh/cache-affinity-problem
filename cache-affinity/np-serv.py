#!/usr/bin/python

import os, sys, SocketServer
  
HOST, PORT = "192.168.0.8", 9994 # It's dumb that you have to specify an address FIXME

class Handler(SocketServer.BaseRequestHandler):

  def handle(self):
    try: 
      # self.request is the TCP socket connected to the client
      self.data = self.request.recv(1024)
      (s_addr, d_addr, s_port, d_port) = self.data.split(' ')
      print  "connection:", (s_addr, d_addr, s_port, d_port) 
    
      # TODO Determine which CPU to map netperf to, send to client.  
      cpu = 0
      self.request.sendall(str(cpu))

    finally: 
      self.request.close()

if __name__ == "__main__":

  # Create the server, binding to localhost on port 9999
  server = SocketServer.TCPServer((HOST, PORT), Handler)

  # Activate the server; this will keep running until you
  # interrupt the program with Ctrl-C
  server.serve_forever()

