import socket
import bz2
import pickle

ip = ""
port = 9999
message = bz2.compress(pickle.dumps("HELLO WORLD"))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message, (ip, port))
