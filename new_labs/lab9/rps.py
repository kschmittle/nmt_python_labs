#!/usr/bin/env python

import select
import socket
import sys
import rps_mom as mom

def main():
    host = ''
    port = 50001
    backlog = 5
    size = 1024
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(backlog)
    inputs = [server, sys.stdin]
    running = True
    while running:
        input_ready, output_ready, except_ready = select.select(inputs, [], [])
        
        for s in input_ready:
            if s == server:
                client, address = server.accept()
                print("Received connection from {}.".format(address))
                inputs.append(client)
                
                mom.add_client(client)

            elif s == sys.stdin:
                #handle standard input
                junk = sys.stdin.readline().strip()
                if junk == 'quit':
                    print("Closing server.")
                    running = False
            else:
                #handle other sockets
                data = s.recv(size)
                print(data)
                if not mom.users[s].recv(data):
                    #this socket closed
                    print("Connection {} closed remotely.".format(s.getpeername()))
                    s.close()
                    inputs.remove(s)
                    mom.remove_client(s)

    server.close()


if __name__ == '__main__':
    main()