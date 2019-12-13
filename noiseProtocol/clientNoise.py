import socket

from noise.connection import NoiseConnection

sock = socket.socket()
sock.connect(('localhost', 2000))

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

# As of now, the handshake should be finished (as we are using NN pattern).
# Any further calls to write_message or read_message would raise NoiseHandshakeError exception.
# We can use encrypt/decrypt methods of NoiseConnection now for encryption and decryption of messages.
encrypted_message = proto.encrypt(b'This is an example payload')
sock.sendall(encrypted_message)

ciphertext = sock.recv(2048)
plaintext = proto.decrypt(ciphertext)
print(plaintext)
