import hashlib
m = hashlib.md5()
m.update(b"1")
md5 =m.hexdigest().upper()

lvl_0 = md5[0:2]
lvl_1 = md5[2:4]
print(lvl_0)
print(lvl_1)