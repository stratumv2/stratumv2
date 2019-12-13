import socket
from itertools import cycle

from noise.connection import NoiseConnection

if __name__ == '__main__':
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('localhost', 2000))
    s.listen(1)

    conn, addr = s.accept()
    print('Accepted connection from', addr)

    noise = NoiseConnection.from_name(b'Noise_NN_25519_ChaChaPoly_SHA256')
    print(noise)
    noise.set_as_responder()
    noise.start_handshake()

    # Perform handshake. Break when finished
    for action in cycle(['receive', 'send']):
        if noise.handshake_finished:
            break
        elif action == 'send':
            ciphertext = noise.write_message()
            #print('cipherText',ciphertext)
            conn.sendall(ciphertext)
        elif action == 'receive':
            data = conn.recv(2048)
            plaintext = noise.read_message(data)
            #print('receive',plaintext)

    # Endless loop "echoing" received data
    while True:
        data = conn.recv(2048)
        if not data:
            break
        received = noise.decrypt(data)
        print(received)
        conn.sendall(noise.encrypt(received))
