from PIL import Image
from Crypto.Cipher import AES

f = open('flag.png.enc', 'rb')
img = Image.frombytes('RGB', (2000, 250), f.read(), decoder_name='raw')
img.save("flag.png")
