# Crypto/Really Solid Algebra

### Challenge

- Category: Crypto
- Autho: null
- Description: Using all the latest math and crypto libraries, this new Really Solid Algebra system should be practically uncrackable!
- Downloads
  - rsa.py
  - output.log

### Writeup by
- hag

---

## Files

```
$ cat rsa.py
```
```python
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from sympy import randprime, nextprime, invert

p = randprime(2**1023, 2**1024)
q = nextprime(p)
n = p * q
e = 65537
phi = (p-1)*(q-1)
d = int(invert(e, phi))
key = RSA.construct((n, e, d, p, q))
rsa = PKCS1_OAEP.new(key)
print(n)
print(rsa.encrypt(open('./flag.txt', 'rb').read()))
```

```
$ cat output.log
13170168669036673658789415835821860466913191064101534501779274940690742604281448647173671946400157617199838272310601920602142822774113607705996734952326957290215951537099625639427739047605224303952391610020730760816940205220160216771511419133822833718461981026872830323755731912443015969055035169814519489784526129811052288823469079931979611710076056973923037676007513769049838507897490490814829478688852449121000733730837518239278607078752774705826529888903312298568894804438251828413144707077871047124974876546688478973141243880671642440976847597210524941636796956020071417167383875898209056473829391281999028768027
b'$\x1f\xcd\x00=\xd8\xe7"w\x92\xf4\xd4_D\xe4\xba\x0be\xc3\x07\xd9/;\xcf\x0eD\xe4UE\xcb\x81\xfb\xd8\xe7\x98\x02\xa1w\xc9#\x84\xcf\x10V\xf6\x8aZ\xad\xee\x1a+Z\xb3Kp\xd3]1\x0f\xb9\x16l\xa6R\xa0uK\x13\xbebtY\xe3Y\xdan\x99\x8d5}\xbai\xd2ss&\xb4h:U\xe4\xf8\x08\xfc)\xfeP\x0c\xa8tq\xd0Y\xd1\x81\xd5\xa2P\xcf\xcd\xee\xb9X<1\xaa\x0f\xcb\x89\x88\x15\xabj\xfc\xec\x05:\xc11\xf3\xc5\xb4"\xa5\x03jy\x9f\x8c\xa0r\xb8\xbcu\x07\xda\xa3\xebt\\w\xa7\xc4x\xe6G\xf3\xc3\x84\xc0U22\xa3a\x80S\x7f\x18>\x04}\xe9\xcd\x97\xe6\x8e\xf8\xf5\x03\x88\x97\xab\x1b\x1b\x1f\xbe7\'\x90P\xbc\'\x02 \xf2.\x18\xce\x89ua\xf6#3PU\xb3\xe5x\xfd\xbd\xf0\x86\xd8\x17U\xd2m\xf8!\xc7\x99e\x12\xdb\xeb\x86\xf4\x14\x833>\xc0\xa2\xdck\x94\xd3\xbc\x05-\xcc\xb6 \x96\xc4C\x1a&\xaf\xcb\xb8.\xcep'
```

## Interesting Parts

So we have `n = 13170168669036673658789415835821860466913191064101534501779274940690742604281448647173671946400157617199838272310601920602142822774113607705996734952326957290215951537099625639427739047605224303952391610020730760816940205220160216771511419133822833718461981026872830323755731912443015969055035169814519489784526129811052288823469079931979611710076056973923037676007513769049838507897490490814829478688852449121000733730837518239278607078752774705826529888903312298568894804438251828413144707077871047124974876546688478973141243880671642440976847597210524941636796956020071417167383875898209056473829391281999028768027` and `e = 65537`. This is the basically the public key.

## RsaCtfTool

We can use `RsaCtfTool` with the public key data and the cipher text to try and recreate the private key and decipher the cipher text.

### Create `key.pub`:

```
$ /opt/RsaCtfTool/RsaCtfTool.py -n 13170168669036673658789415835821860466913191064101534501779274940690742604281448647173671946400157617199838272310601920602142822774113607705996734952326957290215951537099625639427739047605224303952391610020730760816940205220160216771511419133822833718461981026872830323755731912443015969055035169814519489784526129811052288823469079931979611710076056973923037676007513769049838507897490490814829478688852449121000733730837518239278607078752774705826529888903312298568894804438251828413144707077871047124974876546688478973141243880671642440976847597210524941636796956020071417167383875898209056473829391281999028768027 -e 65537 --createpub --private > key.pub
```

### `key.pub`
```
$ cat key.pub
-----BEGIN PUBLIC KEY-----
MIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBoU+zL0fwORcmyxWDfxt70
4rAKC3Q4EsS1AD1Z63sTa5RZ9BxXCwKsxEWtKb2RuslB6sXAOTSR3jpl8N+/ZMKT
LraGZHDp0x0oG1RcIInV9fI+tteLkt0x1SYVOkg/S2Y4Rhixk9otv3/2zfKXwIQj
ElVzpPcjRUlJRWxm3ayJwZamcobFeBquqSR0/3PDVvc1SwLmnl1acWS8pVhfS3Fe
X+0qLcvLTFNaVP09vMZDgm7m2/LUHXB7p/qgndGbkRNbR8GJZ4fu8Q02cjT0/yth
kfhsqVKOZw4DIjyhSQqPrJ0266cdrP3/WwCy6Q98PEKpA67vol8t8KV7PkwzkU0b
AgMBAAE=
-----END PUBLIC KEY-----
```

### Create the `cipher` file with the cipher text from `output.log` Let's just use `bpython` to interactively convert the Python `b''`-string from `output.log` and write it to a binary file

```python
$ bpython
bpython version 0.21 on top of Python 3.9.2 /usr/bin/python3
>>> c = b'$\x1f\xcd\x00=\xd8\xe7"w\x92\xf4\xd4_D\xe4\xba\x0be\xc3\x07\xd9/;\xcf\x0eD\xe4UE\xcb\x81\xfb\xd8\xe7\x98\x02\xa1w\xc9#\x84\xcf\x10V\xf6\x8aZ\xad\xee\x1a+Z\xb3Kp\xd3]1\x0f\xb9\x16l\xa6R\xa0uK\x13\xbebtY\xe3Y\xdan\x99\x8d5}\xbai\xd2ss&\xb4h:U\xe4\xf8\x08\xfc)\xfeP\x0c\xa8tq\xd0Y\xd1\x81\xd5\xa2P\xcf\xcd\xee\xb9X<1\xaa\x0f\xcb\x89\x88\x15\xabj\xfc\xec\x05:\xc11\xf3\xc5\xb4"\xa5\x03jy\x9f\x8c\xa0r\xb8\xbcu\x07\xda\xa3\xebt\\w\xa7\xc4x\xe6G\xf3\xc3\x84\xc0U22\xa3a\x80S\x7f\x18>\x04}\xe9\xcd\x97\xe6\x8e\xf8\xf5\x03\x88\x97\xab\x1b\x1b\x1f\xbe7\'\x90P\xbc\'\x02 \xf2.\x18\xce\x89ua\xf6#3PU\xb3\xe5x\xfd\xbd\xf0\x86\xd8\x17U\xd2m\xf8!\xc7\x99e\x12\xdb\xeb\x86\xf4\x14\x833>\xc0\xa2\xdck\x94\xd3\xbc\x05-\xcc\xb6 \x96\xc4C\x1a&\xaf\xcb\xb8.\xcep'
>>> file = open("cipher", "wb")
>>> file.write(c)
256
>>> file.close()
>>> exit()
?????????(hag???hag-desktop)-[~/ik_equinor_ctf/Crypto/Really Solid Algebra]
??????$ cat cipher
$???=??????"w?????????_D???
               e??????/;???D???UE??????????????w???#??????V??????Z??????+Z???Kp???]1???l???R???uK???btY???Y???n??????5}???i???ss&???h:U??????)???P
                                                                                        ???tq???Y????P?????????X<1???????????j??????:???1?????"???jy?????????r??????u?????t\w??????x???G????????U22???a???S>}???????????????????????7'???P???' ???.??ua???#3PU??????x????????????U???m???!??e????????????3>?????????k?????-?? ??????C&?????.???p
```

### Attacking with `RsaCtfTool.py`

```bash
/opt/RsaCtfTool/RsaCtfTool.py --publickey key.pub --uncipherfile cipher --private

[*] Testing key key.pub.
[*] Performing factordb attack on key.pub.
[*] Performing smallq attack on key.pub.
[*] Performing pastctfprimes attack on key.pub.
100%|???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????| 113/113 [00:00<00:00, 599944.75it/s]
[*] Performing system_primes_gcd attack on key.pub.
100%|?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????| 7007/7007 [00:00<00:00, 732557.84it/s]
[*] Performing mersenne_primes attack on key.pub.
 29%|?????????????????????????????????????????????                                    | 15/51 [00:00<00:00, 385978.90it/s]
[*] Performing fibonacci_gcd attack on key.pub.
100%|????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????| 9999/9999 [00:00<00:00, 76601.47it/s]
[*] Performing pollard_p_1 attack on key.pub.
  0%|                                                               | 0/997 [00:02<?, ?it/s]
[*] Performing SQUFOF attack on key.pub.
[!] Timeout.
[*] Performing fermat attack on key.pub.
[*] Attack success with fermat method !

Results for key.pub:

Private key :
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQBoU+zL0fwORcmyxWDfxt704rAKC3Q4EsS1AD1Z63sTa5RZ9BxX
CwKsxEWtKb2RuslB6sXAOTSR3jpl8N+/ZMKTLraGZHDp0x0oG1RcIInV9fI+tteL
kt0x1SYVOkg/S2Y4Rhixk9otv3/2zfKXwIQjElVzpPcjRUlJRWxm3ayJwZamcobF
eBquqSR0/3PDVvc1SwLmnl1acWS8pVhfS3FeX+0qLcvLTFNaVP09vMZDgm7m2/LU
HXB7p/qgndGbkRNbR8GJZ4fu8Q02cjT0/ythkfhsqVKOZw4DIjyhSQqPrJ0266cd
rP3/WwCy6Q98PEKpA67vol8t8KV7PkwzkU0bAgMBAAECggEAXlXk/Lg3bsB0DY6k
djRhTpXcEHki8cEm1XQOBc0EUR8p2dz980cleAtR5a6kl62KZmxfu9z+SBfmPl98
MphtyKCoswUHhKc86hMsSNGzUSE/lq3GYZK/KFxQP0mgInuPRrs7gPbshglvMEAx
aD7QPNZLJnK4ddAk4HhB+RHg/f5DKfVS7qhBybv1Jnsbbe0V0EE4Dcz2xR/AZZGA
+R5YXm7O7uSkyGq+WslPSFP6hz/5s3/rYj2KNWI1+hEi/ZMZkCNl2qunxlswtjjP
2DUFKYxYNO9DRagcHiF/2zTFqvbOlBlha7Lv+rpRg+nXO7Qd3Eqc5aJaS24AULOd
oOXooQKBgQCjbPPFSVf74l5NWJUdRcmuCEEXmLn6ktajq0zep5rmrDv6dUCafpOA
10t6LRdwXHdPFQbQ/gFIoAUBR2BitysRqcaqoo3ZLpHTTumIwYH+B2w0zP6J0Xvt
AzJBunipo0oUCjBvpw4CEimCW5LHxQFN2/ZfvGKLKPvJ0YlqGqy6DwKBgQCjbPPF
SVf74l5NWJUdRcmuCEEXmLn6ktajq0zep5rmrDv6dUCafpOA10t6LRdwXHdPFQbQ
/gFIoAUBR2BitysRqcaqoo3ZLpHTTumIwYH+B2w0zP6J0XvtAzJBunipo0oUCjBv
pw4CEimCW5LHxQFN2/ZfvGKLKPvJ0YlqGqy4NQKBgFhNX24DEjI8fv3F1lRJyA5r
0VgBosO8oZMv1Modv7nR6FqNDkosCGE+cz7hrF9+5sxpLRSxmln2dJ3bRj4wgGn7
1SePy5tE6XBGnDLTc/yhYBsrhIFNGmvXJUmUiuwGGdm4I7HAjvYZgCo6dpXQYcMD
Dh1uecR9cYb73AbjwN6LAoGAFyLPh/iQKiqr6wtFYPWGTcsBXBPVEHJFTLptkX/s
4Ac2HokG8lhFDZJtLwi/LrsIcPurEV9EU0HEM6AlNxRzVnbQl0uYBU0ge+fKDABJ
JOtsGDWFO4Gap70yGjgJ6Qoi7J9cqBHgW86ybbAFIZ70Rk+Dm54R3V2Z98JgT9Mi
7JkCgYEAgqvouDXIgqZquhBHs314wJ7nWrLTWrdMkOiQGKVWlvSmxqP2oEGP3UwC
j5i2YwXiGOLnvt6KNTVqni/jwFk1VwjUUVjto2RtCaHuk7FoeqS4Rk1+1NABVUYQ
9ee7NqBEaa1psu3PQE5Ag8aFBljuI8pXW6uxFrINYAT5wWVC0UI=
-----END RSA PRIVATE KEY-----

Unciphered data :
HEX : 0x4550547b357172745f62335f73633472795f6f776f7d
INT (big endian) : 25933367355671505200470789025190414914462851232395133
INT (little endian) : 46930960929934061814163788480313995111478633268793413
utf-8 : EPT{5qrt_b3_sc4ry_owo}
utf-16 : ?????????????????????????????????
STR : b'EPT{5qrt_b3_sc4ry_owo}'
HEX : 0x00951fe038f703c7fe9d3feba3c48f01f072f9fa3bd0b21d9d96cdf8d12b4bfcf4938a2caa5c5f6df6e8338d1daf9620364ff409de568e3bef48eb8dabaa79e299eff6f87037b37c1b86040d23cefb6ebd476ce53cabb17ff415f115c99be0f90e05a8dcc1d552f717cb8d67c83e56cf095f82e9e121789cb2e14d6a3ce3e8282adb19b6f6027caea998a3cd8b9b0799bdcd990ce1412f02300b1526a1b34923e981a50913e35a5765089d5a3ef424c8a74968d6b08b1b4cd0674349a070b4ed0954ae51ae4f3e8a3eb4c4f41902c4c3a34921ae994a82b19c373bfc526748bada740a28bfb32e846a752a50dfb91a38895e3f2fcb588843a5b201f850838cb5
INT (big endian) : 73536039128485318980779584866712998906678635090950187669906717847355833506577356717688391792106966031360891628505641027843103096917535250191203583848179099272605114951001941863584454013805997612319496771491475028089794735680312066051603875398920334768756199833776971632753416733913540457304858133494604845355998864730439802819734178788081331510964296773807696727700006364282792381631093964610501190773014746344305121071418078138677210843586577970090450269994018287970838606928843864405443442499807114582034303166165051879135636476879327012043700037274314398198550340956119144168912384532453539650617386385631579317
INT (little endian) : 22918422719045905082451957599076306186486562624196715930448896885817609752914563598963350898739635968074374722882013593784405958117936363125142134479797506253483257883498782169642800584586515704454203567672008564843623133058086326241026765577248360039591405049890271927566520843001572688637001159908498215480020933180562609321607399223844020578251453552709316784700264066870957006289221382803215108074032069734506638534800333047348037159866404138873062750043543340231017048326871430015988452276835085620014823095819127819624357726579588451963519014296095083848882415043274126460848751642407483340057836110933554861312
STR : b'\x00\x95\x1f\xe08\xf7\x03\xc7\xfe\x9d?\xeb\xa3\xc4\x8f\x01\xf0r\xf9\xfa;\xd0\xb2\x1d\x9d\x96\xcd\xf8\xd1+K\xfc\xf4\x93\x8a,\xaa\\_m\xf6\xe83\x8d\x1d\xaf\x96 6O\xf4\t\xdeV\x8e;\xefH\xeb\x8d\xab\xaay\xe2\x99\xef\xf6\xf8p7\xb3|\x1b\x86\x04\r#\xce\xfbn\xbdGl\xe5<\xab\xb1\x7f\xf4\x15\xf1\x15\xc9\x9b\xe0\xf9\x0e\x05\xa8\xdc\xc1\xd5R\xf7\x17\xcb\x8dg\xc8>V\xcf\t_\x82\xe9\xe1!x\x9c\xb2\xe1Mj<\xe3\xe8(*\xdb\x19\xb6\xf6\x02|\xae\xa9\x98\xa3\xcd\x8b\x9b\x07\x99\xbd\xcd\x99\x0c\xe1A/\x020\x0b\x15&\xa1\xb3I#\xe9\x81\xa5\t\x13\xe3ZWe\x08\x9dZ>\xf4$\xc8\xa7Ih\xd6\xb0\x8b\x1bL\xd0gCI\xa0p\xb4\xed\tT\xaeQ\xaeO>\x8a>\xb4\xc4\xf4\x19\x02\xc4\xc3\xa3I!\xae\x99J\x82\xb1\x9c7;\xfcRgH\xba\xdat\n(\xbf\xb3.\x84ju*P\xdf\xb9\x1a8\x89^?/\xcbX\x88C\xa5\xb2\x01\xf8P\x83\x8c\xb5'
```

### `key`

We now have the private key.

```
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQBoU+zL0fwORcmyxWDfxt704rAKC3Q4EsS1AD1Z63sTa5RZ9BxX
CwKsxEWtKb2RuslB6sXAOTSR3jpl8N+/ZMKTLraGZHDp0x0oG1RcIInV9fI+tteL
kt0x1SYVOkg/S2Y4Rhixk9otv3/2zfKXwIQjElVzpPcjRUlJRWxm3ayJwZamcobF
eBquqSR0/3PDVvc1SwLmnl1acWS8pVhfS3FeX+0qLcvLTFNaVP09vMZDgm7m2/LU
HXB7p/qgndGbkRNbR8GJZ4fu8Q02cjT0/ythkfhsqVKOZw4DIjyhSQqPrJ0266cd
rP3/WwCy6Q98PEKpA67vol8t8KV7PkwzkU0bAgMBAAECggEAXlXk/Lg3bsB0DY6k
djRhTpXcEHki8cEm1XQOBc0EUR8p2dz980cleAtR5a6kl62KZmxfu9z+SBfmPl98
MphtyKCoswUHhKc86hMsSNGzUSE/lq3GYZK/KFxQP0mgInuPRrs7gPbshglvMEAx
aD7QPNZLJnK4ddAk4HhB+RHg/f5DKfVS7qhBybv1Jnsbbe0V0EE4Dcz2xR/AZZGA
+R5YXm7O7uSkyGq+WslPSFP6hz/5s3/rYj2KNWI1+hEi/ZMZkCNl2qunxlswtjjP
2DUFKYxYNO9DRagcHiF/2zTFqvbOlBlha7Lv+rpRg+nXO7Qd3Eqc5aJaS24AULOd
oOXooQKBgQCjbPPFSVf74l5NWJUdRcmuCEEXmLn6ktajq0zep5rmrDv6dUCafpOA
10t6LRdwXHdPFQbQ/gFIoAUBR2BitysRqcaqoo3ZLpHTTumIwYH+B2w0zP6J0Xvt
AzJBunipo0oUCjBvpw4CEimCW5LHxQFN2/ZfvGKLKPvJ0YlqGqy6DwKBgQCjbPPF
SVf74l5NWJUdRcmuCEEXmLn6ktajq0zep5rmrDv6dUCafpOA10t6LRdwXHdPFQbQ
/gFIoAUBR2BitysRqcaqoo3ZLpHTTumIwYH+B2w0zP6J0XvtAzJBunipo0oUCjBv
pw4CEimCW5LHxQFN2/ZfvGKLKPvJ0YlqGqy4NQKBgFhNX24DEjI8fv3F1lRJyA5r
0VgBosO8oZMv1Modv7nR6FqNDkosCGE+cz7hrF9+5sxpLRSxmln2dJ3bRj4wgGn7
1SePy5tE6XBGnDLTc/yhYBsrhIFNGmvXJUmUiuwGGdm4I7HAjvYZgCo6dpXQYcMD
Dh1uecR9cYb73AbjwN6LAoGAFyLPh/iQKiqr6wtFYPWGTcsBXBPVEHJFTLptkX/s
4Ac2HokG8lhFDZJtLwi/LrsIcPurEV9EU0HEM6AlNxRzVnbQl0uYBU0ge+fKDABJ
JOtsGDWFO4Gap70yGjgJ6Qoi7J9cqBHgW86ybbAFIZ70Rk+Dm54R3V2Z98JgT9Mi
7JkCgYEAgqvouDXIgqZquhBHs314wJ7nWrLTWrdMkOiQGKVWlvSmxqP2oEGP3UwC
j5i2YwXiGOLnvt6KNTVqni/jwFk1VwjUUVjto2RtCaHuk7FoeqS4Rk1+1NABVUYQ
9ee7NqBEaa1psu3PQE5Ag8aFBljuI8pXW6uxFrINYAT5wWVC0UI=
-----END RSA PRIVATE KEY-----
```

### ... and the deciphered cipher text

```
Unciphered data :
HEX : 0x4550547b357172745f62335f73633472795f6f776f7d
INT (big endian) : 25933367355671505200470789025190414914462851232395133
INT (little endian) : 46930960929934061814163788480313995111478633268793413
utf-8 : EPT{5qrt_b3_sc4ry_owo}
utf-16 : ?????????????????????????????????
STR : b'EPT{5qrt_b3_sc4ry_owo}'
```

### Flag

`EPT{5qrt_b3_sc4ry_owo}`
