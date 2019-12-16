import noiseEncryption

server = noiseEncryption.Noise()

server.HandleNoiseConnection()

data = server.receiveNoiseFrame()

server.sendNoiseFrame(data)
