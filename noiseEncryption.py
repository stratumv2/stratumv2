import socket
from itertools import cycle
import socket
import struct

from noise.connection import NoiseConnection

class Noise:

    def __init__(self):
        self.port = 6222
        self.noise = None
        self.connection = None

    #handling only one connection for the moment
    def HandleNoiseConnection(self):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('localhost', self.port))
        s.listen(1)

        print("Waiting connections...")



        conn, addr = s.accept()
        print('Accepted connection from', addr)

        self.noise = NoiseConnection.from_name(b'Noise_NN_25519_ChaChaPoly_SHA256')

        self.noise.set_as_responder()
        self.noise.start_handshake()

        # Perform handshake. Break when finished
        for action in cycle(['receive', 'send']):
            if self.noise.handshake_finished:
                break
            elif action == 'send':
                ciphertext = self.noise.write_message()
                # print('cipherText',ciphertext)
                conn.sendall(ciphertext)
            elif action == 'receive':
                data = conn.recv(2048)
                plaintext = self.noise.read_message(data)
                # print('receive',plaintext)

        print("Noise handshake finished with",addr)
        self.connection = conn

    def connectToNoise(self,ip,port):

        print('Trying to connect to',ip+":"+str(port))
        sock = socket.socket()
        sock.connect((ip, port))

        # Create instance of NoiseConnection, set up to use NN handshake pattern, Curve25519 for
        # elliptic curve keypair, ChaCha20Poly1305 as cipher function and SHA256 for hashing.
        proto = NoiseConnection.from_name(b'Noise_NN_25519_ChaChaPoly_SHA256')

        # Set role in this connection as initiator
        proto.set_as_initiator()
        # Enter handshake mode
        proto.start_handshake()

        # Perform handshake - as we are the initiator, we need to generate first message.
        # We don't provide any payload (although we could, but it would be cleartext for this pattern).
        message = proto.write_message()
        # Send the message to the responder - you may simply use sockets or any other way
        # to exchange bytes between communicating parties.
        sock.sendall(message)
        # Receive the message from the responder
        received = sock.recv(2048)
        # Feed the received message into noise
        payload = proto.read_message(received)

        self.connection = sock
        self.noise = proto

    def sendNoiseFrame(self,frame):
        self.connection.sendall(self.noise.encrypt(frame))

    def receiveNoiseFrame(self):

        #2097158 = 2+1+3+(2**(24-3) max size of frame
        data = self.connection.recv(2097158)
        received = self.noise.decrypt(data)
        return received

    def closeNoiseConnection(self):
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
        self.connection.close()



