#!/usr/bin/python

import os, sys, socket

if len(sys.argv) != 5: 
  print >> sys.stderr, "usage: np-client.py <s_addr> <d_addr> <s_port> <d_port>"
  sys.exit(1)

(s_addr, d_addr, s_port, d_port) = sys.argv[1:]
HOST, PORT = (d_addr, 9994)

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:

  sock.connect((HOST, PORT))

  # Send connection information to server, wait for cpu to map to. 
  sock.sendall(' '.join(sys.argv[1:]))
  cpu = int(sock.recv(1024))

finally:
  sock.close()

os.system("netperf -H %s -L %s -t UDP_STREAM -l 10 -c -C -T ,%d -- -m 1448 \
          -k throughput,local_sd,remote_sd,elapsed_time -P %s,%s" % 
          (d_addr, s_addr, cpu, s_port, d_port))

