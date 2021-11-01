# Crypto/Arbitrary Encoding System

### Challenge

- Category: Crypto
- Author: null
- Description: I heard that all the cool kids down the street had switched to this new cipher. Think it was called Arbitrary Encoding System or something...
- Downloads
  - aes.py
  - flag.png.enc

### Writeup by
- hag

---

## Files

`$ cat aes.py`
```python
from PIL import Image
from Crypto.Cipher import AES

img = Image.open('flag.png')
assert img.mode == 'RGB'
assert img.height == 250
assert img.width == 2000
assert str([b for rgb in [[1, 2, 3], [4, 5, 6], [7, 8, 9]] for b in rgb]) == '[1, 2, 3, 4, 5, 6, 7, 8, 9]'
data = bytes([b for rgb in img.getdata() for b in rgb])  # flatten
assert len(data) % 16 == 0
key = open('/dev/urandom', 'rb').read(16)
aes = AES.new(key, AES.MODE_ECB)
ct = aes.encrypt(data)
open('flag.png.enc', 'wb').write(ct)
```

`flag.png.enc` is the encrypted image we want to retrieve.



## AES.MODE_ECB

We can see that the image has been encryptet with `AES.MODE_ECB`. `ECB` is not a safe mode for encryption. The classic "ECB Penguin" shows why:

![](ecbpenguin.png "")

I think we can see the flag in the encrypted image `flag.png.enc` if we can convert it into a working image.

We can't open the encrypted file as is:

![](imageerr.png "")

As we can see in the `aes.py` script, only the pixel data has been encrypted, but the encrypted file doesn't contain an image header.

We need to recreate the image header and add the encrypted pixel data. Luckily we know the image size and format from the information in the `aes.py` script.


## createflagimg.py

```python
from PIL import Image
from Crypto.Cipher import AES

f = open('flag.png.enc', 'rb')
img = Image.frombytes('RGB', (2000, 250), f.read(), decoder_name='raw')
img.save("flag.png")

```

Our script reads in the encrypted pixel data and creates a new image with the correct dimensions. Let's run our script.


```bash
$ python3 createflagimg.py
```

And look at the created `flag.png`:

![](flag.png "")

The flag is still readable even if the image data is encrypted!


## Flag

`EPT{mode_of_operation_is_important}`